"""PWN contract tests. Every generated row is a synthetic software fixture.

Run from the repository root with ``python -m unittest discover -s tests``.
No tank or Arctic observation is represented by these fixtures.
"""
import csv
import hashlib
import io
import unittest

from backend.pwn import analyze_profile, detect_layers, parse_profile, simulated_profile_csv


HEADER = (
    "schema_version,source_kind,device_id,experiment_id,cast_id,sample_index,"
    "timestamp_utc,elapsed_ms,raw_conductivity_signal,temperature_C,encoder_count,"
    "cable_out_m,pressure_dbar,latitude,longitude,calibration_id,quality_flag"
).split(",")
KIND = "SIMULATION_EXPLANATORY"


def fixture_rows(count=11):
    return [dict(zip(HEADER, [
        "1.0", KIND, "TEST-SIMULATOR", "synthetic-unit-test", "SIM-TEST", i,
        "", i * 1000, 100 if i < 5 else 900, 20, i * 10,
        i / 10, "", "", "", "", "OK",
    ])) for i in range(count)]


def encode_rows(rows, fields=HEADER):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def parse(raw, **options):
    return parse_profile(raw, options.get("source_kind", KIND),
                         options.get("raw_unit", "adc_count_12bit"),
                         options.get("depth_method", "encoder_vertical_tank"))


class ProfileParserTests(unittest.TestCase):
    def test_valid_profile_preserves_raw_values_and_identity(self):
        raw = encode_rows(fixture_rows())
        result = parse(raw)
        self.assertEqual(result["sample_count"], 11)
        self.assertEqual(result["source_kind"], KIND)
        self.assertEqual(result["raw_conductivity_unit"], "adc_count_12bit")
        self.assertEqual(result["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(result["rows"][0]["raw_conductivity_signal"], 100)
        self.assertEqual(result["rows"][-1]["raw_conductivity_signal"], 900)
        self.assertIsNone(result["rows"][0]["latitude"])
        self.assertIsNone(result["rows"][0]["pressure_dbar"])
        self.assertNotIn("salinity", result["rows"][0])

    def test_missing_measurement_is_not_zero_filled(self):
        rows = fixture_rows()
        rows[2].update(raw_conductivity_signal="", temperature_C="",
                       quality_flag="MISSING_CONDUCTIVITY;MISSING_TEMPERATURE")
        result = parse(encode_rows(rows))
        self.assertIsNone(result["rows"][2]["raw_conductivity_signal"])
        self.assertIsNone(result["rows"][2]["temperature_C"])
        self.assertTrue(result["warnings"])

    def test_utf8_bom_accepted_but_invalid_utf8_rejected(self):
        raw = encode_rows(fixture_rows())
        self.assertEqual(parse(b"\xef\xbb\xbf" + raw)["sample_count"], 11)
        with self.assertRaises(ValueError):
            parse(b"\xff\xfe")

    def test_missing_required_header_and_empty_file_rejected(self):
        for raw in (b"", b"device_id,raw_conductivity_signal\nX,1\n",
                    encode_rows([])):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse(raw)

    def test_extra_column_rejected(self):
        raw = encode_rows(fixture_rows(1)).rstrip(b"\n") + b",extra\n"
        with self.assertRaises(ValueError):
            parse(raw)

    def test_truncated_row_rejected(self):
        lines = encode_rows(fixture_rows(1)).decode().splitlines()
        raw = (lines[0] + "\n" + lines[1].rsplit(",", 1)[0] + "\n").encode()
        with self.assertRaises(ValueError):
            parse(raw)

    def test_duplicate_header_rejected(self):
        lines = encode_rows(fixture_rows(1)).decode().splitlines()
        raw = (lines[0] + ",raw_conductivity_signal\n" + lines[1] + ",999\n").encode()
        with self.assertRaises(ValueError):
            parse(raw)

    def test_nonfinite_and_malformed_numbers_rejected(self):
        for field in ("raw_conductivity_signal", "temperature_C", "cable_out_m",
                      "pressure_dbar", "latitude", "longitude", "elapsed_ms"):
            for value in ("NaN", "Inf", "-Infinity", "not-a-number"):
                rows = fixture_rows(1)
                rows[0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    parse(encode_rows(rows))

    def test_negative_distance_pressure_or_elapsed_time_rejected(self):
        for field in ("cable_out_m", "pressure_dbar", "elapsed_ms"):
            rows = fixture_rows(1)
            rows[0][field] = -1
            with self.subTest(field=field), self.assertRaises(ValueError):
                parse(encode_rows(rows))

    def test_signed_encoder_counts_are_allowed(self):
        rows = fixture_rows(1)
        rows[0]["encoder_count"] = -4
        self.assertEqual(parse(encode_rows(rows))["rows"][0]["encoder_count"], -4)

    def test_fractional_counts_and_elapsed_time_rejected(self):
        for field in ("sample_index", "encoder_count", "elapsed_ms"):
            rows = fixture_rows(1)
            rows[0][field] = "1.5"
            with self.subTest(field=field), self.assertRaises(ValueError):
                parse(encode_rows(rows))

    def test_sample_index_and_elapsed_time_cannot_go_backwards(self):
        for field, value in (("sample_index", 0), ("elapsed_ms", 500)):
            rows = fixture_rows(3)
            rows[2][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                parse(encode_rows(rows))

    def test_utc_only_rows_accepted_and_invalid_utc_rejected(self):
        rows = fixture_rows(2)
        for index, row in enumerate(rows):
            row.update(elapsed_ms="", timestamp_utc=f"2026-01-01T00:00:0{index}Z")
        self.assertEqual(parse(encode_rows(rows))["sample_count"], 2)
        for value in ("", "bad-date", "2026-01-01T00:00:00",
                      "2026-01-01T00:00:00+03:00", "2025-12-31T23:59:59Z"):
            rows[1]["timestamp_utc"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse(encode_rows(rows))

    def test_mixed_cast_device_or_source_rejected(self):
        for field, value in (("cast_id", "ANOTHER-CAST"), ("device_id", "OTHER-DEVICE"),
                             ("source_kind", "OUR_NEW_MEASUREMENT_TANK")):
            rows = fixture_rows(2)
            rows[1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                parse(encode_rows(rows))

    def test_planned_observation_unknown_unit_and_method_rejected(self):
        raw = encode_rows(fixture_rows())
        for options in ({"source_kind": "PLANNED_ARCTIC_OBSERVATION"},
                        {"raw_unit": "PSU"}, {"depth_method": "cable_is_ocean_depth"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                parse(raw, **options)

    def test_unavailable_depth_does_not_promote_cable_length(self):
        result = parse(encode_rows(fixture_rows()), depth_method="unavailable")
        self.assertEqual(result["rows"][-1]["cable_out_m"], 1)
        self.assertTrue(all(row["derived_depth_m"] is None for row in result["rows"]))


class GradientBaselineTests(unittest.TestCase):
    def test_constant_profile_has_no_layer(self):
        result = detect_layers([i / 10 for i in range(11)], [42] * 11)
        self.assertEqual(result["status"], "analyzed")
        self.assertEqual(result["layers"], [])

    def test_independent_step_fixture_finds_transition_without_accuracy_claim(self):
        result = detect_layers([i / 10 for i in range(11)], [100] * 5 + [900] * 6)
        self.assertEqual(result["status"], "analyzed")
        self.assertEqual(len(result["layers"]), 1)
        self.assertGreaterEqual(result["layers"][0]["depth_m"], 0.4)
        self.assertLessEqual(result["layers"][0]["depth_m"], 0.5)
        self.assertGreater(result["layers"][0]["gradient"], 0)
        self.assertEqual(result["threshold_units"], "raw_signal_unit/m")
        self.assertIsNone(result["boundary_error_m"])
        self.assertIsNone(result["confidence"])

    def test_upcast_and_downcast_give_same_gradient(self):
        depth = [i / 10 for i in range(11)]
        signal = [100] * 5 + [900] * 6
        down = detect_layers(depth, signal)
        up = detect_layers(depth[::-1], signal[::-1])
        self.assertEqual(up["depth_m"], down["depth_m"])
        self.assertEqual(up["gradient"], down["gradient"])
        self.assertEqual(up["layers"], down["layers"])

    def test_duplicate_or_mixed_direction_depth_is_not_silently_sorted(self):
        for depth in ([0, 0.1, 0.1, 0.3, 0.4], [0, 0.2, 0.1, 0.3, 0.4]):
            with self.subTest(depth=depth):
                result = detect_layers(depth, [1, 1, 4, 4, 4])
                self.assertEqual(result["status"], "insufficient_data")
                self.assertEqual(result["layers"], [])

    def test_insufficient_or_nonfinite_pairs_are_not_analyzed(self):
        for depth, signal in (([0, 1, 2], [1, 1, 4]),
                              ([0, 1, 2, 3, 4], [1, 2]),
                              ([0, 1, 2, 3, 4], [1, 2, float("nan"), 4, 5])):
            with self.subTest(depth=depth, signal=signal):
                self.assertEqual(detect_layers(depth, signal)["status"], "insufficient_data")

    def test_raw_signal_never_becomes_ec_salinity_or_trained_ai(self):
        raw = encode_rows(fixture_rows())
        result = analyze_profile(raw, KIND, "adc_count_12bit", "encoder_vertical_tank")
        self.assertIsNone(result["derived_ec"])
        self.assertIsNone(result["derived_salinity"])
        self.assertFalse(result["adaptive_sampling"]["ai_trained"])
        self.assertEqual(result["adaptive_sampling"]["status"], "proposal_only")
        self.assertEqual(result["source_kind"], KIND)
        self.assertEqual(result["sha256"], hashlib.sha256(raw).hexdigest())

    def test_quality_flag_excludes_gradient_without_erasing_raw_row(self):
        rows = fixture_rows()
        rows[4]["quality_flag"] = "ADC_SATURATED"
        result = analyze_profile(encode_rows(rows), KIND, "adc_count_12bit", "encoder_vertical_tank")
        self.assertEqual(result["sample_count"], 11)
        self.assertEqual(result["excluded_from_gradient"], 1)
        self.assertEqual(result["rows"][4]["quality_flag"], "ADC_SATURATED")

    def test_demo_fixture_is_explicitly_simulated(self):
        raw = simulated_profile_csv()
        rows = list(csv.DictReader(io.StringIO(raw.decode())))
        self.assertTrue(rows)
        self.assertEqual(set(row["source_kind"] for row in rows), {KIND})
        result = analyze_profile(raw, KIND, "V", "encoder_vertical_tank")
        self.assertEqual(len(result["analysis"]["layers"]), 1)
        self.assertAlmostEqual(result["analysis"]["layers"][0]["depth_m"], 0.3)
        self.assertIsNone(result["derived_salinity"])


if __name__ == "__main__":
    unittest.main()
