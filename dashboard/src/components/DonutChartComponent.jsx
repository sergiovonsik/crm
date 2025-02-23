import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import PropTypes from 'prop-types';

const DonutChartComponent = ({data, title, colors}) => {
    return (
        <div className="p-4 flex items-center justify-center">
            <h2> {title ?  title : "TEST"}</h2>
            <div className="bg-white p-4 rounded-lg shadow-md flex flex-col items-center justify-center" style={{ width: 350, height: 350 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={data}
                            dataKey="value"
                            nameKey="category"
                            cx="50%"
                            cy="50%"
                            innerRadius={80}
                            outerRadius={120}
                            fill="#8884d8"
                            paddingAngle={5}
                            label
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                            ))}
                        </Pie>
                        <Tooltip />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

DonutChartComponent.propTypes = {
    title: PropTypes.string,
    data: PropTypes.arrayOf(
        PropTypes.shape({
            category: PropTypes.string.isRequired,
            value: PropTypes.number.isRequired,
        })
    ).isRequired,
    colors: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default DonutChartComponent;
