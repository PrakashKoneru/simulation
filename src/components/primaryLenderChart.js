import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
	Legend,
	ErrorBar
	} from "recharts";
	
	const CustomizedLabel = (props) => {
		const { x, y, index } = props;
		
		if(index === 4) {
			return (
				<text x={x} y={y} dx={-30} dy={0} fill={'#8884d8'} fontSize={20} textAnchor="middle">
					Paisa
				</text>
			);
		}
		return null;
	};

  function PrimaryLenderChart({ data, paisaDataKey, currentDataKey, paisaErrorKey, keyHelper }) {
		let prevValue;
		const ticksArray = data.map((each, index) => {
			let roundedValue = Math.round(((each[paisaErrorKey] + each[paisaDataKey]) + each[currentDataKey]) / 2)
			if(prevValue === roundedValue) {
				prevValue = roundedValue = roundedValue + 1;
			} else {
				prevValue = roundedValue;
			}
			return roundedValue;
		})
		const finalTickValue = Math.round(data[4][paisaDataKey] + data[4][paisaErrorKey] + 0.4)

    return(
			<div key={Math.random()}>
				<LineChart
					width={420}
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
					<YAxis
						ticks={[...ticksArray, finalTickValue]}
						interval={0}
						domain={[dataMin => (Math.round(dataMin - 0.4)), dataMax => (Math.round(dataMax + 0.4))]}
					/>
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
					>
						<ErrorBar
							dataKey={paisaErrorKey}
							width={4}
							strokeWidth={2}
							stroke="green"
							direction="y"
						/>
					</Line>
				</LineChart>
			</div>
    )
  };

  export default PrimaryLenderChart;