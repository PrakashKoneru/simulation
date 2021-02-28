import React from 'react';
import styled from 'styled-components';
import LogoImg from './logo.png';
import useScrollTrigger from "@material-ui/core/useScrollTrigger";
import CssBaseline from '@material-ui/core/CssBaseline';

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


function ElevationScroll(props) {
	const { children, window } = props;
	// Note that you normally won't need to set the window ref as useScrollTrigger
	// will default to window.
	// This is only being set here because the demo is in an iframe.
	const trigger = useScrollTrigger({
	  disableHysteresis: true,
	  threshold: 0,
	  target: window ? window() : undefined,
	});
  
	return React.cloneElement(children, {
	  elevation: trigger ? 4 : 0,
	});
  }

export default function Header(props) {
	return (
		<>
			<CssBaseline />
			<ElevationScroll {...props}>
				<HeaderContainer>
					<Logo>
						<img src={LogoImg} height={50} width={155} alt='Paisa Logo' />
					</Logo>
				</HeaderContainer>
			</ElevationScroll>
		</>
	)
}