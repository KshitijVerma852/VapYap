import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const SetupPage = () => {
	const [motion, setMotion] = useState("");
	const [infoSlide, setInfoSlide] = useState("");
	const [position, setPosition] = useState("OG");
	const navigate = useNavigate();

	const handleSubmit = async (event) => {
		event.preventDefault();

		const formData = {
			motion,
			infoSlide,
			position
		};
		const url = "http://localhost:8000";
		try {
			console.log(formData);
			const response = await fetch(url, {
				method: "POST",
				headers: {
					"Content-type": "application/json"
				},
				body: JSON.stringify({
					motion,
					infoSlide,
					position
				})
			});
			if (!response.ok) {
				console.log("We fucked up");
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			navigate("/speech", { state: { ...formData } });
		} catch (error) {
			navigate("/speech", { state: { ...formData } });
			console.error("There was an error with the request:", error);
		}
	};


	return (
		<div>
			<h1 style={{ color: "pink" }}>Vap Yap</h1>
			<form style={{ maxWidth: "600px", margin: "auto" }} onSubmit={handleSubmit}>
				<div style={{ marginBottom: "20px" }}>
					<label htmlFor="motion" style={{ display: "block", marginBottom: "10px" }}>Motion:</label>
					<textarea
						id="motion"
						cols="30"
						rows="10"
						value={motion}
						onChange={(e) => setMotion(e.target.value)}
						style={{ width: "100%", padding: "10px", resize: "none" }}
						required={true}
					/>
				</div>
				<div style={{ marginBottom: "20px" }}>
					<label htmlFor="infoSlide" style={{ display: "block", marginBottom: "10px" }}>InfoSlide:</label>
					<textarea
						id="infoSlide"
						cols="30"
						rows="10"
						value={infoSlide}
						onChange={(e) => setInfoSlide(e.target.value)}
						style={{ width: "100%", padding: "10px", resize: "none" }}
						placeholder={"(optional)"}
					/>
				</div>
				<div style={{ marginBottom: "20px" }}>
					<label htmlFor="position" style={{ display: "block", marginBottom: "10px" }}>Position:</label>
					<select
						id="position"
						value={position}
						onChange={(e) => setPosition(e.target.value)}
						style={{ width: "100%", padding: "10px" }}
						required={true}
					>
						<option value="OG">OG</option>
						<option value="OO">OO</option>
						<option value="CG">CG</option>
						<option value="CO">CO</option>
					</select>
				</div>
				<button
					type={"submit"}
					style={{
						padding: "15px 30px",
						fontSize: "18px",
						color: "black",
						background: "pink",
						border: "none",
						borderRadius: "25px",
						cursor: "pointer",
						display: "block",
						marginLeft: "auto",
						marginRight: "auto"
					}}
				>
					Submit
				</button>
			</form>
		</div>
	);
};

export default SetupPage;
