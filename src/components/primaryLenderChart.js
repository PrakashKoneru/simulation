import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
	} from "recharts";
	
	const CustomizedLabel = (props) => {
		const { x, y, index } = props;
		
		if(index === 4) {
			return (
				<text x={x} y={y} dx={20} dy={-7} fill={'#8884d8'} fontSize={20} textAnchor="middle">
					Paisa
				</text>
			);
		}
		return null;
	};

  function PrimaryLenderChart({ data, paisaDataKey, currentDataKey }) {
    return(
			<div>
				<LineChart
					width={375}
					height={375}
					data={data}
					margin={{
						top: 50,
						right: 70,
						left: 20,
						bottom: 75
					}}
				>
					<CartesianGrid strokeDasharray="3 3" />
					<XAxis dataKey="inv_time_periods_yrs" />
					<YAxis />
					<Tooltip />
					<Line
						type="monotone"
						dataKey={currentDataKey}
						stroke="#82ca9d"
						activeDot={{ r: 8 }}
					/>
					<Line
						type="monotone"
						dataKey={paisaDataKey}
						label={<CustomizedLabel />}
						stroke="#8884d8"
						strokeWidth={2}
					/>
				</LineChart>
			</div>
    )
  };

  export default PrimaryLenderChart;