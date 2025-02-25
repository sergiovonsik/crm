import {useState} from "react";
import PropTypes from "prop-types";
import "../styles/RangeSlider.css"; // Import CSS
import RangeSlider from 'react-range-slider-input';
import 'react-range-slider-input/dist/style.css';

function TimeSlider({ rangeOfDates, setRangeOfDates }) {
    return (

        <div className="component-container">

            <h2> Set the range of time</h2>

            <div className="slider-wrapper">
            {/* Button on the left
             <div className="refresh-button">Refresh charts</div>
             */}


            {/* Slider on the right */}
            <div className="slider-container">
                {/* First Thumb Label */}

                <div
                    className="thumb-label-top"
                    style={{ left: `${((rangeOfDates[0] + 120) / 135) * 100}%` }}
                >
                    {new Date(new Date().setDate(new Date().getDate() + rangeOfDates[0])).toLocaleDateString()}
                </div>

                {/* Second Thumb Label */}
                <div
                    className="thumb-label-bottom"
                    style={{ left: `${((rangeOfDates[1] + 120) / 135) * 100}%` }}
                >
                    {new Date(new Date().setDate(new Date().getDate() + rangeOfDates[1])).toLocaleDateString()}
                </div>

                {/* Slider */}
                <RangeSlider
                    id="range-slider-yellow"
                    min={-120}
                    max={15}
                    step={1}
                    value={[rangeOfDates[0], rangeOfDates[1]]}
                    onInput={setRangeOfDates}
                    onChange={console.log(rangeOfDates)}
                />
            </div>
        </div>

        </div>
    );
}

TimeSlider.propTypes = {
    rangeOfDates: PropTypes.arrayOf(PropTypes.number).isRequired,
    setRangeOfDates: PropTypes.func.isRequired,
};

export default TimeSlider;
