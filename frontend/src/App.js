import React from "react";
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import './App.css';
import SetupPage from "./pages/SetupPage";
import SpeechPage from "./pages/SpeechPage";

function App() {
	return (
		<div className="App">
			<header className="App-header">
				<Router>
					<Routes>
						<Route path="/" element={<SetupPage/>}/>
						<Route path="/speech" element={<SpeechPage />} />
					</Routes>
				</Router>
			</header>
		</div>
	);
}

export default App;
