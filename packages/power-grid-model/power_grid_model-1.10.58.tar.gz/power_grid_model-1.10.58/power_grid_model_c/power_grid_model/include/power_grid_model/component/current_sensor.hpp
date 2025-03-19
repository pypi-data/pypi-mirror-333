// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

#pragma once

#include "sensor.hpp"

#include "../calculation_parameters.hpp"
#include "../common/common.hpp"
#include "../common/enum.hpp"
#include "../common/exception.hpp"
#include "../common/statistics.hpp"

namespace power_grid_model {

class GenericCurrentSensor : public Sensor {
  public:
    static constexpr char const* name = "generic_current_sensor";

    explicit GenericCurrentSensor(GenericCurrentSensorInput const& generic_current_sensor_input)
        : Sensor{generic_current_sensor_input},
          terminal_type_{generic_current_sensor_input.measured_terminal_type},
          angle_measurement_type_{generic_current_sensor_input.angle_measurement_type} {}

    MeasuredTerminalType get_terminal_type() const { return terminal_type_; }
    AngleMeasurementType get_angle_measurement_type() const { return angle_measurement_type_; }

    template <symmetry_tag sym> CurrentSensorOutput<sym> get_output(ComplexValue<sym> const& i) const {
        if constexpr (is_symmetric_v<sym>) {
            return get_sym_output(i);
        } else {
            return get_asym_output(i);
        }
    }

    template <symmetry_tag sym> CurrentSensorOutput<sym> get_null_output() const {
        return {.id = id(), .energized = false, .i_residual = {}, .i_angle_residual = {}};
    }

    SensorShortCircuitOutput get_null_sc_output() const { return {.id = id(), .energized = 0}; }

    // getter for calculation param
    template <symmetry_tag sym> CurrentSensorCalcParam<sym> calc_param() const {
        if constexpr (is_symmetric_v<sym>) {
            return sym_calc_param();
        } else {
            return asym_calc_param();
        }
    }

  protected:
    MeasuredTerminalType terminal_type() const { return terminal_type_; }
    AngleMeasurementType angle_measurement_type() const { return angle_measurement_type_; }

  private:
    MeasuredTerminalType terminal_type_;
    AngleMeasurementType angle_measurement_type_;

    // virtual function getter for sym and asym param
    // override them in real sensors function
    virtual CurrentSensorCalcParam<symmetric_t> sym_calc_param() const = 0;
    virtual CurrentSensorCalcParam<asymmetric_t> asym_calc_param() const = 0;

    virtual CurrentSensorOutput<symmetric_t> get_sym_output(ComplexValue<symmetric_t> const& i) const = 0;
    virtual CurrentSensorOutput<asymmetric_t> get_asym_output(ComplexValue<asymmetric_t> const& i) const = 0;
};

template <symmetry_tag current_sensor_symmetry_> class CurrentSensor : public GenericCurrentSensor {
  public:
    using current_sensor_symmetry = current_sensor_symmetry_;

    static constexpr char const* name =
        is_symmetric_v<current_sensor_symmetry> ? "sym_current_sensor" : "asym_current_sensor";
    using InputType = CurrentSensorInput<current_sensor_symmetry>;
    using UpdateType = CurrentSensorUpdate<current_sensor_symmetry>;
    template <symmetry_tag sym_calc> using OutputType = CurrentSensorOutput<sym_calc>;

    explicit CurrentSensor(CurrentSensorInput<current_sensor_symmetry> const& current_sensor_input, double u_rated)
        : GenericCurrentSensor{current_sensor_input},
          base_current_{base_power_3p * inv_sqrt3 / u_rated},
          base_current_inv_{1.0 / base_current_},
          i_angle_measured_{current_sensor_input.i_angle_measured},
          i_angle_sigma_{current_sensor_input.i_angle_sigma},
          i_sigma_{current_sensor_input.i_sigma * base_current_inv_},
          i_measured_{current_sensor_input.i_measured * base_current_inv_} {
        switch (current_sensor_input.measured_terminal_type) {
            using enum MeasuredTerminalType;
        case branch_from:
        case branch_to:
        case branch3_1:
        case branch3_2:
        case branch3_3:
            break;
        default:
            throw InvalidMeasuredTerminalType{current_sensor_input.measured_terminal_type, "Current sensor"};
        }
    };

    UpdateChange update(CurrentSensorUpdate<current_sensor_symmetry> const& update_data) {
        assert(update_data.id == this->id() || is_nan(update_data.id));

        update_real_value<symmetric_t>(update_data.i_sigma, i_sigma_, base_current_inv_);
        update_real_value<symmetric_t>(update_data.i_angle_sigma, i_angle_sigma_, 1.0);
        update_real_value<current_sensor_symmetry>(update_data.i_measured, i_measured_, base_current_inv_);
        update_real_value<current_sensor_symmetry>(update_data.i_angle_measured, i_angle_measured_, 1.0);

        return {false, false};
    }

    CurrentSensorUpdate<current_sensor_symmetry>
    inverse(CurrentSensorUpdate<current_sensor_symmetry> update_data) const {
        assert(update_data.id == this->id() || is_nan(update_data.id));

        set_if_not_nan(update_data.i_sigma, i_sigma_ * base_current_);
        set_if_not_nan(update_data.i_angle_sigma, i_angle_sigma_);
        set_if_not_nan(update_data.i_measured, i_measured_ * base_current_);
        set_if_not_nan(update_data.i_angle_measured, i_angle_measured_);

        return update_data;
    }

  private:
    double base_current_{};
    double base_current_inv_{};
    RealValue<current_sensor_symmetry> i_angle_measured_{};
    double i_angle_sigma_{};
    double i_sigma_{};
    RealValue<current_sensor_symmetry> i_measured_{};

    CurrentSensorCalcParam<symmetric_t> sym_calc_param() const final { return calc_decomposed_param<symmetric_t>(); }
    CurrentSensorCalcParam<asymmetric_t> asym_calc_param() const final { return calc_decomposed_param<asymmetric_t>(); }

    template <symmetry_tag sym_calc> CurrentSensorCalcParam<sym_calc> calc_decomposed_param() const {
        auto const i_polar = PolarComplexRandVar<current_sensor_symmetry>(
            {i_measured_, i_sigma_ * i_sigma_}, {i_angle_measured_, i_angle_sigma_ * i_angle_sigma_});
        auto const i_decomposed = DecomposedComplexRandVar<sym_calc>(i_polar);
        return CurrentSensorCalcParam<sym_calc>{.angle_measurement_type = angle_measurement_type(),
                                                .value = i_decomposed.value(),
                                                .i_real_variance = i_decomposed.real_component.variance,
                                                .i_imag_variance = i_decomposed.imag_component.variance};
    }
    CurrentSensorOutput<symmetric_t> get_sym_output(ComplexValue<symmetric_t> const& i) const final {
        return get_generic_output<symmetric_t>(i);
    }
    CurrentSensorOutput<asymmetric_t> get_asym_output(ComplexValue<asymmetric_t> const& i) const final {
        return get_generic_output<asymmetric_t>(i);
    }
    template <symmetry_tag sym_calc>
    CurrentSensorOutput<sym_calc> get_generic_output(ComplexValue<sym_calc> const& i) const {
        CurrentSensorOutput<sym_calc> output{};
        output.id = id();
        ComplexValue<sym_calc> const i_residual{process_mean_val<sym_calc>(i_measured_ - i) * base_current_};
        output.energized = 1; // current sensor is always energized
        output.i_residual = cabs(i_residual);
        output.i_angle_residual = arg(i_residual);
        return output;
    }
};

using SymCurrentSensor = CurrentSensor<symmetric_t>;
using AsymCurrentSensor = CurrentSensor<asymmetric_t>;

} // namespace power_grid_model
