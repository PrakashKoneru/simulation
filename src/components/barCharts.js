import React, { useState, useEffect } from 'react';
import { useForm } from "react-hook-form";
import { Flex } from '../library/Flex';
import PrimaryLenderChart from './primaryLenderChart';

function BarCharts({ apiResults }) {
	const { register, watch, handleSubmit } = useForm();

	const [selectedKpi, updateSelectedKpi] = useState('lenderReturns')


	const inv_time_periods_yrs = [3, 4, 5, 6, 7];
	const grades = ["Grade A", "Grade B", "Grade C", "Grade D"];

	if(apiResults) {
		
		var lenderReturnsGraphs = Object.keys(apiResults).map((key, index) => {
			let result = []
			for (let i=0; i<5; i++) {
				result.push({
					inv_time_periods_yrs: inv_time_periods_yrs[i],
					current_abs_return: apiResults[key]['current_abs_return'][i],
					paisa_abs_return_mean: apiResults[key]['paisa_abs_return_mean'][i],
					paisa_abs_return_std: apiResults[key]['paisa_abs_return_std'][i]
				})
			}
			return result;
		});

		var platformRevenueGraphs = Object.keys(apiResults).map((key, index) => {
			let result = []
			for (let i=0; i<5; i++) {
				result.push({
					inv_time_periods_yrs: inv_time_periods_yrs[i],
					current_lrr: apiResults[key]['current_lrr'][i],
					paisa_lrr_mean: apiResults[key]['paisa_lrr_mean'][i],
					paisa_lrr_std: apiResults[key]['paisa_lrr_std'][i]
				})
			}
			return result;
		});

		var platformEfficiencyGraphs = Object.keys(apiResults).map((key, index) => {
			let result = []
			for (let i=0; i<5; i++) {
				result.push({
					inv_time_periods_yrs: inv_time_periods_yrs[i],
					current_llr: apiResults[key]['current_llr'][i],
					paisa_llr_mean: apiResults[key]['paisa_llr_mean'][i],
					paisa_llr_std: apiResults[key]['paisa_llr_std'][i]
				})
			}
			return result;
		});



		console.log(lenderReturnsGraphs, platformRevenueGraphs, platformEfficiencyGraphs);
		
		// updatePrimaryLenderReturns(primaryLenderReturnsArray);
		// updatePlatformRevenue(platformRevenueArray)
		// updatePlatformEfficiency(platformEfficiencyArray)
	}

	return (
		<div>
			<Flex
				style={{
					alignItems: 'flex-end',
					padding: '0px 30px',
					marginTop: '40px'
				}}
			>
				<div
					style={{
						width: '30px',
						padding: '0px 40px'
					}}
				>
					KPIs:
				</div>
				<div
					style={{
						marginTop: '30px',
						width: '70%',
						padding: '0px 60px 0px 0px'
					}}
				>
					<form onSubmit={handleSubmit(() => {})}>
						<Flex>
							<Flex style={{ alignItems: 'center', marginRight: '50px' }}>
								<input
									name="bargraphs"
									type="radio"
									ref={register}
									value="lenderReturns"
									onClick={(e) => { updateSelectedKpi(e.target.value) }}
									checked={selectedKpi === 'lenderReturns'}
								/>
								<label for="lenderReturns">Lender Returns</label>
							</Flex>
							<Flex style={{ alignItems: 'center', marginRight: '50px' }}>
								<input
									name="bargraphs"
									type="radio"
									value="platformRevenue"
									ref={register}
									onClick={(e) => { updateSelectedKpi(e.target.value) }}
								/>
								<label for="platformRevenue">Platform Revenue</label>
							</Flex>
							<Flex style={{ alignItems: 'center', marginRight: '5px' }}>
								<input
									name="bargraphs"
									type="radio"
									value="platformEfficiency"
									ref={register}
									onClick={(e) => { updateSelectedKpi(e.target.value) }}
								/>
								<label for="platformEfficiency">Platform Efficiency</label>
							</Flex>
						</Flex>
					</form>
				</div>
			</Flex>
			<div
				style={{
					marginLeft: '-35px',
					marginTop:' 50px'
				}}
			>
				{selectedKpi === 'lenderReturns' && apiResults && lenderReturnsGraphs && (
					<Flex style={{ justifyContent: 'space-between'}}>
							{lenderReturnsGraphs.map((lenderReturnsGraph, index) => {
								return (
									<div style={{ width: '25%'}}>
										<PrimaryLenderChart 
											data={lenderReturnsGraph}
											currentDataKey={'current_abs_return'}
											paisaDataKey={'paisa_abs_return_mean'}
											paisaErrorKey={'paisa_abs_return_std'}
											grade={grades[index]}
										/>
									</div>
								)
							})}
					</Flex>
				)}
				{selectedKpi === 'platformRevenue' && apiResults && (
					<Flex style={{ justifyContent: 'space-between'}}>
							{platformRevenueGraphs.map((platformRevenueGraph, index) => {
								return (
									<div style={{ width: '25%'}}>
										<PrimaryLenderChart
											data={platformRevenueGraph}
											currentDataKey={'current_lrr'}
											paisaDataKey={'paisa_lrr_mean'}
											paisaErrorKey={'paisa_lrr_std'}
											grade={grades[index]}
										/>
									</div>
								)
							})}
					</Flex>
				)}
				{selectedKpi === 'platformEfficiency' && apiResults &&(
					<Flex style={{ justifyContent: 'space-between'}}>
							{platformEfficiencyGraphs.map((platformEfficiencyGraph, index) => {
								return (
									<div style={{ width: '25%', position: 'relative' }}>
										<PrimaryLenderChart 
											data={platformEfficiencyGraph}
											currentDataKey={'current_llr'}
											paisaDataKey={'paisa_llr_mean'}
											paisaErrorKey={'paisa_llr_std'}
											grade={grades[index]}
										/>
									</div>
								)
							})}
					</Flex>
				)}
			</div>
			{/* <div>
        {primaryLenderReturns && (
          <div style={{ marginTop: '75px' }}>
            <PrimaryLenderChart
              data={primaryLenderReturns}
              paisaDataKey={'paisa_abs_return'}
              currentDataKey={'current_abs_return'}
            />
          </div>
        )}
        {platformRevenue && (
          <div style={{ marginTop: '75px' }}>
            <PrimaryLenderChart
              data={platformRevenue}
              paisaDataKey={'paisa_lrr'}
              currentDataKey={'current_lrr'}
            />
          </div>
        )}
        {platformEfficiency && (
          <div style={{ marginTop: '75px' }}>
            <PrimaryLenderChart
              data={platformEfficiency}
              paisaDataKey={'paisa_llr'}
              currentDataKey={'current_llr'}
            />
          </div>
        )}
      </div> */}
		</div>
	)
}

export default BarCharts;