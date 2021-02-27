import React from 'react';
import styled from 'styled-components';
import CurrentPlatform from '../assets/frame.svg';

const ImageContainer = styled.div`
	margin-top: 50px;
`
const Image = styled.img`
	display: block;
	margin: auto;
	object-fit: contain;
	width: 80%;
	height: 375px;
`

function BlockDiagrams () {
	return (
		<div>
			<ImageContainer>
				<Image src={CurrentPlatform} />
			</ImageContainer>
		</div>
	)
}

export default BlockDiagrams;