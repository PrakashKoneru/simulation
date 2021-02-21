import styled from 'styled-components'

const InputElement = styled.input`
  width: 100%;
  outline: rgba(224,210,210, 0.6);
  padding: 10px;
  border-radius: 2px;
  border: 1.5px solid rgba(224,210,210, 0.6);
  margin-top: 10px;
`;

function Input({ register, ...props }) { 
  return (
    <InputElement
      {...props}
      ref={register} //Strictly revisit passing down refs or move away from react-hooks-form library
    />
  )
}

export default Input;