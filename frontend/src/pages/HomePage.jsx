import React, { useState } from 'react'
import axios from 'axios';

const HomePage = () => {
  const[cv,setCV]=useState("");
  const[jd,setJD]=useState("");
  const[track,setTrack]=useState(null);

  const handleSubmit=async (e)=>{
    e.preventDefault();
    const response = await axios.post('http://127.0.0.1:5000/match',{
      cv:cv,
      jd:jd,
    })
    setTrack(response.data.track)
  }
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
    </div>
  )
}

export default HomePage