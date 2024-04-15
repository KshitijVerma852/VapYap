import React, {useState} from "react";
import {useLocation} from "react-router-dom";

const SpeechPage = () => {
	const location = useLocation();
	const formData = location.state || {};

	const handleCardSubmit = (cardId) => {
		console.log(`Submitting content for card ${cardId}`);
	};


	const Card = ({id, title}) => {
		const [content, setContent] = useState('');

		return (
			<div
				style={{margin: '20px', padding: '20px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', borderRadius: '8px'}}>
				<h4 style={{fontSize: '24px', marginBottom: '10px'}}>{title}</h4>
				<textarea
					value={content}
					onChange={(e) => setContent(e.target.value)}
					style={{width: '100%', padding: '10px', marginBottom: '10px'}} cols="30"
					rows="10"
				/>
				<button
					type={"submit"}
					style={{
						padding: '15px 30px',
						fontSize: '18px',
						color: 'black',
						background: 'pink',
						border: 'none',
						borderRadius: '25px',
						cursor: 'pointer',
						display: 'block',
						marginLeft: 'auto',
						marginRight: 'auto'
					}}
				>
					Submit
				</button>
			</div>
		);
	};

	return (
		<div style={{textAlign: 'center', padding: '20px'}}>
			<h1 style={{fontSize: '32px', color: 'pink'}}>Motion: {formData.motion || 'N/A'}</h1>
			<h1 style={{fontSize: '32px', color: 'pink'}}>InfoSlide: {formData.infoSlide || 'N/A'}</h1>
			<h1 style={{fontSize: '32px', color: 'pink'}}>Position: {formData.position || 'N/A'}</h1>

			<div style={{display: 'flex', justifyContent: 'center', flexWrap: 'wrap'}}>
				<Card id="motionCard1" title="PM"/>
				<Card id="motionCard2" title="LO"/>
				<Card id="infoSlideCard1" title="DPM"/>
				<Card id="infoSlideCard2" title="DLO"/>
			</div>

			<div style={{display: 'flex', justifyContent: 'center', flexWrap: 'wrap'}}>
				<Card id="positionCard1" title="MG"/>
				<Card id="positionCard2" title="MO"/>
				<Card id="positionCard1" title="GW"/>
				<Card id="positionCard2" title="OW"/>
			</div>

		</div>
	);
};

export default SpeechPage;
