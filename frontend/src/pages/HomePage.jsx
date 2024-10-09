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
    <div>HomePage</div>
  )
}

export default HomePage