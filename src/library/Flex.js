import React from 'react';
import styled from 'styled-components';

const FlexStyles = styled.div`
	display: flex;
`;

export function Flex({ children, ...rest }) {
	return (
		<FlexStyles {...rest}>
			{children}
		</FlexStyles>
	)
}

export function FlexItem({ children }) {
	return(
		{children}
	)
}
