import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import { useForm } from "react-hook-form";
import Input from './library/input';
import Button from '@material-ui/core/Button';
import Header from './components/header';
import PrimaryLenderChart from './components/primaryLenderChart';

function App() {
  const { register, handleSubmit } = useForm();
  const [simulationData, updateSimulationData] = useState(null);
  const [primaryLenderReturns, updatePrimaryLenderReturns] = useState(null)
  const [platformRevenue, updatePlatformRevenue] = useState(null)
  const [platformEfficiency, updatePlatformEfficiency] = useState(null)

  const postData = async (data) => {
    axios
    .post('http://127.0.0.1:5000/simulate', {
      formData: {
        loan_grade: "A",
        inv_time_periods: [3, 4, 5, 6, 7],
        ...data
      }
    })
    .then((response) => {
      const current_abs_return = response.data['current_abs_return'];
      const paisa_abs_return = response.data['paisa_abs_return'];
      const xAxisValues = [3, 4, 5, 6, 7];

      const primaryLenderReturns = xAxisValues.map((each, index) => {
        return {
          inv_time_periods: each,
          current_abs_return: response.data['current_abs_return'][index],
          paisa_abs_return: response.data['paisa_abs_return'][index]
        }
      })

      const platformRevenue = xAxisValues.map((each, index) => {
        return {
          inv_time_periods: each,
          current_lrr: response.data['current_lrr'][index],
          paisa_lrr: response.data['paisa_lrr'][index]
        }
      })

      const platformEfficiency = xAxisValues.map((each, index) => {
        return {
          inv_time_periods: each,
          current_llr: response.data['current_llr'][index],
          paisa_llr: response.data['paisa_llr'][index]
        }
      })

      updatePrimaryLenderReturns(primaryLenderReturns);
      updatePlatformRevenue(platformRevenue)
      updatePlatformEfficiency(platformEfficiency)
    })
  }

  return (
    <div className="App">
      <Header />
      <form onSubmit={handleSubmit(postData)}>
        <div>
          <Input
            name="defaults_present"
            placeholder="defaults_present"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="current_orig_percent"
            placeholder="current_orig_percent"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="current_comm_percent"
            placeholder="current_comm_percent"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="paisa_orig_percent"
            placeholder="paisa_orig_percent"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="paisa_comm_percent"
            placeholder="paisa_comm_percent"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="emi_reinvest_period"
            placeholder="emi_reinvest_period"
            pattern="^-?[0-9]\d*\.?\d*$"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="principal"
            placeholder="principal"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Input
            name="principal_grow_percent"
            placeholder="principal_grow_percent"
            type='number'
            register={register({
              valueAsNumber: true,
            })}
            step="any"
          />
          <Button color="primary" variant="contained" type="submit">Send Details</Button>
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
        </div>
      </form>
    </div>
  );
}

export default App;
