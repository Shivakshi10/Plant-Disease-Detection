import { useCallback, useEffect, useState } from 'react';
import './homepage.css';
import { useDropzone } from 'react-dropzone';


const Homepage = () => {


const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState({});
    const [img, setImg] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setImg(file);
    if (file) {
      const objectUrl = URL.createObjectURL(file);
      setPreviewUrl(objectUrl);
    }
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", img);
  
//     const res = await fetch("http://127.0.0.1:5000/predict", {
//       method: "POST",
//       body: formData,
//     });
  
//  const datas = await res.json();
//  setData(datas);
//  console.log(data);
//     console.log(data.class);
//     setIsLoading(false); // Contains prediction result

try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    });

    const datas = await res.json();
    setData(datas);
    console.log(datas.class);
  } catch (error) {
    setData("Prediction error");
  } finally {
    setIsLoading(false); // Stop loading regardless of success/failure
  }
};


  const handleReset = () => {
    setImg(null);
    setPreviewUrl(null);
    setData({});
  };


return (
    <div className="Home">
    <div className="left">
        <span className='span'onClick={handleReset} style={{ cursor: 'pointer' }}>Plant Disease Detection System</span>
        <span className='span1'>Snap. Detect. Protect. — Instantly Identify Plant Diseases with a Single Click!</span>
    </div>
    <div className="right">
        <div className='file-upload'>
            <div className="upload-container">
                <div className="upload-icon">
                    <img className='upload' src='./upload.png' alt=""></img>
                </div>
                <input type='file' className='file-input' onChange={handleFileUpload}></input>
            </div>
            {previewUrl && (
            <div className="preview-container">
              <h4>Image Preview:</h4>
              <div className='imgContainer'><img src={previewUrl} alt="Preview" style={{ width: '300px', marginTop: '10px' }} /></div>
              
            
            <button className='submitButton' onClick={handleSubmit}> Submit</button>
            {isLoading && <div className="resultname">Loading prediction...</div>}
            </div>
          )}
          
          { Object.keys(data).length > 0 && (
                <div className='Result'>
                    <span className='resultname'>result : {data.class}</span>
                </div>
             )} 
        </div>
       
    </div>
    </div>);
  }
  
  export default Homepage;