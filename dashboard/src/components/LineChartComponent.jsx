import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";

function LineChartComponent({ chartData, lineColor, title }) {
    const [multipleVariables, setMultipleVariables] = useState(false);

    useEffect(() => {
        if (chartData.length > 0 && chartData[0].free_climb_value !== undefined && chartData[0].classes_value !== undefined) {
            setMultipleVariables(true);
        }
    }, [chartData]);

    return (
        <div className="p-4">
            {/* Line Chart */}
            <div className="bg-white p-4 rounded-lg shadow-md mb-6">
                <h2 className="text-xl font-semibold mb-2">Performance of {title} over time</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke={lineColor} strokeWidth={7} strokeOpacity={0.8} />

                        {/* Correct conditional rendering */}
                        {multipleVariables && (
                            <>
                                <Line type="monotone" dataKey="free_climb_value"
                                      stroke="#0077ff" strokeWidth={3} strokeOpacity={1} />
                                <Line type="monotone" dataKey="classes_value"
                                      stroke="#069707" strokeWidth={3} strokeOpacity={1} />

                            </>
                        )}
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

LineChartComponent.propTypes = {
    chartData: PropTypes.arrayOf(
        PropTypes.shape({
            date: PropTypes.string.isRequired,
            value: PropTypes.number.isRequired,
            free_climb_value: PropTypes.number,
            classes_value: PropTypes.number,
        })
    ).isRequired,
    lineColor: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
};

export default LineChartComponent;
