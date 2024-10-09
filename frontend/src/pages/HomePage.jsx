import React, { useState,useEffect  } from 'react'
import axios from 'axios';

const HomePage = () => {
  const[cv,setCV]=useState("");
  const[jd,setJD]=useState("");
  const[track,setTrack]=useState(null);
  const [matches, setMatches] = useState([]);

  const handleSubmit=async (e)=>{
    e.preventDefault();
    try{
      const response = await axios.post('http://127.0.0.1:5000/match',{
        cv:cv,
        jd:jd,
      })
      setTrack(response.data.track)
      fetchMatches();
    
    
  }catch (error) {
    console.error("Error submitting data:", error);
  }
};



const fetchMatches = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/matches');
    setMatches(response.data);
  } catch (error) {
    console.error("Error fetching matches:", error);
  }
};

useEffect(() => {
  fetchMatches();
}, []);
  return (
    <div>
      <div>
        <form onSubmit={handleSubmit}>
        <div>
        <label>Resume Text:</label>
        <textarea value={cv} onChange={(e) => setCV(e.target.value)} />
      </div>
      <div>
        <label>Job Description:</label>
        <textarea value={jd} onChange={(e) => setJD(e.target.value)} />
      </div>
      <button type="submit">Scan</button>
        </form>
        {track && <p>Similarity Score: {track}</p>}
      </div>
      <h2>Stored Matches</h2>
      <ul>
        {matches.map((match, index) => (
          <li key={index}>
            <p><strong>Resume:</strong> {match.resume}</p>
            <p><strong>Job Description:</strong> {match.job_description}</p>
            <p><strong>Similarity Score:</strong> {match.similarity_score}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default HomePage