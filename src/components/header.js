import React from 'react';
import styled from 'styled-components';
import LogoImg from './logo.png';

const HeaderContainer = styled.div`
	display: flex;
	padding: 8px 10px;
	align-items: center;
	border-bottom: 0.3px solid rgba(224,210,210, 0.6);
	position: relative;
	user-select: none;
`;

const Logo = styled.div`
	display: flex;
	width: 100%;
	font-size: 45px;
	font-weight: 400;
	letter-spacing: 1px;
	align-items: baseline;
`;

export default function Header() {
	return (
		<HeaderContainer>
			<Logo>
				<img src={LogoImg} height={50} width={155} alt='Paisa Logo' />
			</Logo>
		</HeaderContainer>
	)
}