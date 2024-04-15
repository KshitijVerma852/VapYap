import React, {useState} from "react";

const SetupPage = () => {
	const [motion, setMotion] = useState('');
	const [infoSlide, setInfoSlide] = useState('');
	const [position, setPosition] = useState('option1');

	const handleSubmit = async (event) => {
		event.preventDefault();

		const formData = {
			motion,
			infoSlide,
			position
		};
		const url = "http://localhost:8000";
		try {
			const response = await fetch(url, {
				method: "POST",
				headers: {
					"Content-type": "application/json"
				},
				body: JSON.stringify(formData)
			});
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
		} catch (error) {
			console.error("There was an error with the request:", error);
		}
	};



	return (
		<div>
			<h1 style={{color: "pink"}}>Vap Yap</h1>
			<form style={{maxWidth: '600px', margin: 'auto'}} onSubmit={handleSubmit}>
				<div style={{marginBottom: '20px'}}>
					<label htmlFor="motion" style={{display: 'block', marginBottom: '10px'}}>Motion:</label>
					<textarea
						id="motion"
						cols="30"
						rows="10"
						value={motion}
						onChange={(e) => setMotion(e.target.value)}
						style={{width: '100%', padding: '10px', resize: "none"}}
						required={true}
					/>
				</div>
				<div style={{marginBottom: '20px'}}>
					<label htmlFor="infoSlide" style={{display: 'block', marginBottom: '10px'}}>InfoSlide:</label>
					<textarea
						id="infoSlide"
						cols="30"
						rows="10"
						value={infoSlide}
						onChange={(e) => setInfoSlide(e.target.value)}
						style={{width: '100%', padding: '10px', resize: "none"}}
						placeholder={"(optional)"}
					/>
				</div>
				<div style={{marginBottom: '20px'}}>
					<label htmlFor="position" style={{display: 'block', marginBottom: '10px'}}>Position:</label>
					<select
						id="position"
						value={position}
						onChange={(e) => setPosition(e.target.value)}
						style={{width: '100%', padding: '10px'}}
						required={true}
					>
						<option value="option1">OG</option>
						<option value="option2">OO</option>
						<option value="option3">CG</option>
						<option value="option3">CO</option>
					</select>
				</div>
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
			</form>
		</div>
	);
};

export default SetupPage;
