import styled from 'styled-components'

const InputElement = styled.input`
  outline: rgba(224,210,210, 0.6);
  border-radius: 2px;
  border: 1.5px solid rgba(224,210,210, 0.6);
  border-radius: 3px;
  height: 2px;
  padding: 18px 10px;
`;

function Input({ register, ...props }) { 
  return (
    <InputElement
      {...props}
      ref={register} //Strictly revisit passing down refs or move away from react-hooks-form library
      autoComplete="on"
    />
  )
}

export default Input;