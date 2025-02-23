import {useState} from "react";
import PropTypes from "prop-types";
import "../styles/RangeSlider.css"; // Import CSS
import RangeSlider from 'react-range-slider-input';
import 'react-range-slider-input/dist/style.css';

function TimeSlider({rangeOfDates, setRangeOfDates}) {

  return (
      <div className="slider-container">
        {/* First Thumb Label */}
        <div className="thumb-label" style={{left: `${((rangeOfDates[0] + 120) / 135) * 100}%`}}>
          {new Date(new Date().setDate(new Date().getDate() + rangeOfDates[0])).toLocaleDateString()}
        </div>

        {/* Second Thumb Label */}
        <div className="thumb-label" style={{left: `${((rangeOfDates[1] + 120) / 135) * 100}%`}}>
          {new Date(new Date().setDate(new Date().getDate() - rangeOfDates[1])).toLocaleDateString()}
        </div>

        <RangeSlider
            id="range-slider-yellow"
            min={-120}
            max={15}
            step={1}
            value={rangeOfDates}
            onInput={setRangeOfDates}
        />
      </div>
  );
}

TimeSlider.propTypes = {
};

export default TimeSlider;
