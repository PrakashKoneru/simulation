import React from 'react';
import styled from 'styled-components';

const SelectElement = styled.select`
	position: relative;
	border: 1px solid #0079C6;
	border-radius: 3px;
	cursor: pointer;
	border-radius: 5px;
	width: 100%;
	padding: 8px;
	-o-appearance: none;
	-ms-appearance: none;
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	&:active {
		border: 1px solid #0079C6;
	}
`;

const OptionElement = styled.option`
	border: 1px solid rgba(224,210,210, 0.6);
`;

const DropDownIcon = styled.div`
	position: absolute;
	z-index: 20;
	top: 10px;

`;

export function Select ({ register, children, ...rest }) {	
	return (
		<SelectElement ref={register} {...rest}>
			<>
				{children}
				<DropDownIcon> 2 </DropDownIcon>
			</>
		</SelectElement>
	);
}

export function Option({ children, ...rest }) {
	return (
		<OptionElement {...rest}>
			{ children }
		</OptionElement>
	)
}
