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

  function PrimaryLenderChart({ grade, data, paisaDataKey, currentDataKey, paisaErrorKey, keyHelper }) {
		// let prevValue;
		// const ticksArray = data.map((each, index) => {
		// 	let roundedValue = Math.round(((each[paisaErrorKey] + each[paisaDataKey]) + each[currentDataKey]) / 2)
		// 	if(prevValue === roundedValue) {
		// 		prevValue = roundedValue = roundedValue + 1;
		// 	} else {
		// 		prevValue = roundedValue;
		// 	}
		// 	return roundedValue;
		// })
		// const finalTickValue = Math.round(data[4][paisaDataKey] + data[4][paisaErrorKey] + 0.4)

		let minValue = data[0][currentDataKey]
		let maxValue = ([data[4][currentDataKey], data[4][paisaDataKey] + data[4][paisaErrorKey]].sort())[1]

		let tickArrayInterval = (maxValue - minValue) / 5;
		let tickCountHelper = minValue;
		let ticksArray = data.map((each) => {
			tickCountHelper = tickCountHelper + tickArrayInterval;
			// return (Math.round(tickCountHelper * 10)) / 10
			return (Math.round(tickCountHelper + 0.4))
		})
		console.log('tickArrayInterval: ', tickArrayInterval, "ticksArray: ", ticksArray)
    return(
			<div
				key={Math.random()}
				style={{
					position: 'relative'
				}}
			>
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
					<Tooltip
						formatter={(value, name, props) => ([Math.round(value * 100) / 100, "Current",])}
					/>
					<Tooltip
						formatter={(value, name, props) => ([Math.round(value * 100) / 100, "Paisa"])}
					/>
					<XAxis dataKey="inv_time_periods_yrs" />
					<YAxis
						ticks={[Math.round(minValue), ...ticksArray]}
						interval={0}
						domain={[dataMin => (Math.round(dataMin - 0.4)), dataMax => (Math.round(dataMax + 0.4))]}
					/>
					<Line
						type="monotone"
						dataKey={currentDataKey}
						stroke="#82ca9d"
						activeDot={{ r: 8 }}
					>
					</Line>
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
				<div
					style={{
						position: 'absolute',
						bottom: '60px',
						left: '185px'
					}}
				>
					{grade}
				</div>
			</div>
    )
  };

  export default PrimaryLenderChart;