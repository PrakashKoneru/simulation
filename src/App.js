import React, { useState } from 'react';
import axios from 'axios';
import { useForm } from "react-hook-form";
import styled from 'styled-components';
import Button from '@material-ui/core/Button';
import Input from './library/input';
import { Flex } from './library/Flex';
import { Select, Option } from './library/select'
import Header from './components/header';
import { Label } from 'recharts';
import BlockDiagrams from './components/blockDiagrams';
import './App.css';
import BarCharts from './components/barCharts.js'

const InputSideLabel = styled.label`
  text-align: left;
`

const Grid = styled.div`
  display: flex;
  padding: 0px 25px;
	flex-wrap: wrap;
	width: 100%;
  font-size: 14px;
  justify-content: space-between;
`
const Col = styled.div`
  width: 20%;
  padding: 10px;
`

const BorderDiv = styled.div`
  border: 1.5px solid rgba(224,210,210, 0.6);
  padding: 15px;
  margin-right: 15px;
`
const BoxTitle = styled.div`
  padding: 15px;
  margin-right: 15px;
`

const defaultFormValues = [
  {scenario_flag: 1},
  {
    scenario_flag: 2,
    default_flag: 'auto',
    principal: 14000,
    emi_reinvest_period: 12,
    inv_period: '',
    current_orig_percent: 2,
    current_comm_percent: 1.5,
    current_interest_percent: 0,        
    paisa_orig_percent: 2,
    paisa_comm_percent: 1.5, 
    paisa_interest_percent: 0
  },
  {
    scenario_flag: 3,
    default_flag: 'auto',
    principal: 14000,
    emi_reinvest_period: 12,
    inv_period: '',
    current_orig_percent: 2,
    current_comm_percent: 1.5,
    current_interest_percent: 0,
    paisa_orig_percent: 0,
    paisa_comm_percent: 1.5,
    paisa_interest_percent: 0
  },
  {
    scenario_flag: 4,
    principal: 14000,
    default_flag: 'auto',
    emi_reinvest_period: 12,
    inv_period: '',
    current_orig_percent: 2,
    current_comm_percent: 1.5,
    current_interest_percent: 0,
    paisa_orig_percent: 0,
    paisa_comm_percent: 1.5,
    paisa_interest_percent: 0
  },
]

const disableRules = [
  {scenario_flag: 1},
  {
    scenario_flag: 2,
    default_flag: 'auto',
    principal: 14000,
    emi_reinvest_period: 12,
    inv_period: '',
    current_orig_percent: 2,
    current_comm_percent: 1.5,
    current_interest_percent: 0,        
    paisa_orig_percent: 2,
    paisa_comm_percent: 1.5, 
    paisa_interest_percent: 0
  },
  {
    scenario_flag: 3,
    default_flag: 'auto',
    principal: 14000,
    emi_reinvest_period: 12,
    inv_period: '',
    current_orig_percent: 2,
    current_comm_percent: 1.5,
    current_interest_percent: 0,
    paisa_orig_percent: 0,
    paisa_comm_percent: 1.5,
    paisa_interest_percent: 0
  },
  {
    scenario_flag: 4,
    principal: 14000,
    default_flag: 'auto',
    emi_reinvest_period: 12,
    inv_period: '',
    current_orig_percent: 2,
    current_comm_percent: 1.5,
    current_interest_percent: 0,
    paisa_orig_percent: 0,
    paisa_comm_percent: 1.5,
    paisa_interest_percent: 0
  },
]

function App() {
  const [apiResults, updateApiResults] = useState(null);
  const [simulationModel, setSimulationModel] = useState(1);
  const { register, watch, reset, handleSubmit } = useForm();

  const defaultSelcted = watch("default_flag");
  const scenarioSelected = watch("scenario_flag")

  const disableFields = scenarioSelected == 2 || scenarioSelected == 3 || (scenarioSelected == 4 && defaultSelcted === "auto");
  

  const postData = async (data) => {
    axios
    .post('http://127.0.0.1:5000/simulate', {
      formData: {
        inv_time_periods_yrs: [3, 4, 5, 6, 7],
        ...data
      }
    })
    .then((response) => {
      console.log('response: ', response);
      updateApiResults(response.data)
    })
    return 
  }

  return (
    <div className="App" style={{ paddingBottom: '100px'}}>
      <Header />
      <BlockDiagrams />
      <form onSubmit={handleSubmit(postData)} autocomplete="on">
        <Flex style={{ padding: '0px 30px', marginTop: '40px'}}>
          <div style={{ width: '30%', padding: '0px 30px' }}>
            <Flex style={{ alignItems: 'baseline'}}>
              <div style={{ marginRight: '25px'}}>Scenario</div>
              <Select
                name="scenario_flag"
                register={register({
                  valueAsNumber: true,
                })}
                onChange={(e) => {
                  reset(defaultFormValues[e.target.value - 1])
                }}
              >
                <Option value={1}>No Simulation</Option>
                <Option value={2}>Simulation Model</Option>
                <Option value={3}>Borrower Friendly</Option>
                <Option value={4}>Custom</Option>
              </Select>
            </Flex>
            <Flex style={{ marginTop: '25px' }}>
              <div style={{ marginRight: '25px'}}>Defaults</div>
              <div>
                <Flex style={{ justifyContent: 'space-between' }}>
                  <Flex style={{ alignItems: 'center', marginRight: '5px' }}>
                    <input
                      name="default_flag"
                      type="radio"
                      ref={register}
                      value="off"
                      disabled={scenarioSelected != 1}
                    />
                    <label for="off">Off</label>
                  </Flex>
                  <Flex style={{ alignItems: 'center', marginRight: '5px' }}>
                    <input
                      name="default_flag"
                      type="radio"
                      value="auto"
                      ref={register}
                    />
                    <label for="auto">Auto</label>
                  </Flex>
                </Flex>
                <div style={{ marginTop: '15px', minWidth: '168px' }}>
                  <Flex style={{ alignItems: 'center', marginRight: '5px' }}>
                    <input
                      name="default_flag"
                      type="radio"
                      ref={register}
                      value="custom"
                      disabled={scenarioSelected != 4}
                    />
                    <label for="custom">
                      {defaultSelcted === 'custom' ? 'Custom (%)' : 'Custom'}
                    </label>
                  </Flex>
                  {defaultSelcted === 'custom' && (
                    <Input
                      style={{ 
                        width: '10px !important',
                        marginTop: '5px'
                      }}
                      name="default_deviate_percent"
                      register={register({
                        valueAsNumber: true,
                      })}
                      placeholder=">= 0"
                    />
                  )}
                </div>
              </div>
            </Flex>
          </div>
          <div
            style={{ 
              width: '70%',
              padding: '0 60px 0 0'
            }}
          >
            <Flex>
              <div>
                <BoxTitle
                  style={{
                    backgroundColor: '#A5DEFF',
                    border: '1.5px solid #A5DEFF'
                  }}>
                    Lender
                  </BoxTitle>
                <BorderDiv>
                  <div>
                    <div style={{ marginBottom: '8px' }}>Funds ($)</div>
                    <Input
                      name="principal"
                      placeholder="> 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                  <div style={{ marginTop: '15px'}}>
                    <div style={{ marginBottom: '8px' }}>Reinvestment Frequency (Mo.)</div>
                    <Input
                      name="emi_reinvest_period"
                      placeholder="1 - 36"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                  <div style={{ marginTop: '15px'}}>
                    <div style={{ marginBottom: '8px' }}>Investment Period (Yrs.)</div>
                    <Input
                      name="inv_period"
                      placeholder="3 to 7"
                      type='text'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                    />
                  </div>
                </BorderDiv>
              </div>
              <div>
                <BoxTitle
                  style={{
                    backgroundColor: '#FFE2E2',
                    border: '1.5px solid #FFE2E2'
                  }}
                >
                  Current Platform
                </BoxTitle>
                <BorderDiv>
                  <div>
                    <div style={{ marginBottom: '8px' }}>Origination (%)</div>
                    <Input
                      name="current_orig_percent"
                      placeholder=">= 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                  <div style={{ marginTop: '15px'}}>
                    <div style={{ marginBottom: '8px' }}>Commission (%)</div>
                    <Input
                      name="current_comm_percent"
                      placeholder=">= 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                  <div style={{ marginTop: '15px'}}>
                    <div style={{ marginBottom: '8px' }}>Interest Rate (%)</div>
                    <Input
                      name="current_interest_percent"
                      placeholder="> 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                </BorderDiv>
              </div>
              <div>
              <BoxTitle
                style={{
                  backgroundColor: '#FFF617',
                  border: '1.5px solid #FFF617'
                }}
              >
                Paisa
              </BoxTitle>
                <BorderDiv>
                  <div>
                    <div style={{ marginBottom: '8px' }}>Origination (%)</div>
                    <Input
                      name="paisa_orig_percent"
                      placeholder=">= 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                  <div style={{ marginTop: '15px'}}>
                    <div style={{ marginBottom: '8px' }}>Commission (%)</div>
                    <Input
                      name="paisa_comm_percent"
                      placeholder=">= 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginRight: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                  <div style={{ marginTop: '15px'}}>
                    <div style={{ marginBottom: '8px' }}>Interest Rate (%)</div>
                    <Input
                      name="paisa_interest_percent"
                      placeholder="> 0"
                      type='number'
                      register={register({
                        valueAsNumber: true,
                      })}
                      step="any"
                      style={{ width: '200px', marginright: '40px' }}
                      disabled={disableFields}
                    />
                  </div>
                </BorderDiv>
              </div>
            </Flex>
            <Flex
              style = {{
                justifyContent: 'flex-end',
                marginTop: '25px'
              }}
            >
              <div>
                <Button
                  color="primary"
                  variant="contained"
                  type="submit"
                  style={{ whiteSpace: 'nowrap' }}
                >
                  Start Simulation
                </Button>
              </div>
            </Flex>
          </div>
        </Flex>
      </form>
      <BarCharts apiResults={apiResults} />
    </div>
  );
}

export default App;
