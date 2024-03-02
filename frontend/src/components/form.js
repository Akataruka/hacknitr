import React, { useState } from 'react';
import axios from 'axios';
import "./form.css";

const ImageForm = () => {
    const [image, setImage] = useState(null);
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [response, setResponse] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('image', image);
        formData.append('age', age);
        formData.append('gender', gender);

        try {
            const response = await axios.post('/api/predict', formData);
            setResponse(response.data);
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };

    const handleAgeChange = (e) => {
        setAge(e.target.value);
    };

    const handleGenderChange = (e) => {
        setGender(e.target.value);
    };

    return (
        <form onSubmit={handleSubmit}>
          <input type="file" accept="image/*" onChange={handleImageChange} />
          <input type="number" value={age} onChange={handleAgeChange} placeholder="Age" />
          <input type="text" value={gender} onChange={handleGenderChange} placeholder="Gender" />
          <button type="submit">Submit</button>
          {response && <p>Response from server: {response}</p>}
        </form>
      );
    };
    
    export default ImageForm;