import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";


import PropTypes from 'prop-types';

function LineChartComponent({chartData, lineColor, title}){
    return (
        <div className="p-4">
            {/* Line Chart */}
            <div className="bg-white p-4 rounded-lg shadow-md mb-6">
                <h2 className="text-xl font-semibold mb-2">Performance Over Time of {title}</h2>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Line type="monotone" dataKey="value" stroke={lineColor} strokeWidth={3} />
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
        })
    ).isRequired,
    lineColor: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
};

export default LineChartComponent;