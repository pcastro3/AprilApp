import { useState } from 'react';
import Api from '../Api';

function Register() {

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: ''
  })

  const handleInputChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    })
  }

  const handleFormSubmit = async (event) => {
    event.preventDefault();

      await Api.post('/users/', formData);

      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        password: ''
      })
  }  

  return (
    <>
      <h1 className='mb-5'>Register</h1>
      <div className="formContainer">
        <form onSubmit={handleFormSubmit}>

          <div>
            <label>First Name</label>
            <input type="text" className='form-control' id='fName' name='first_name' onChange={handleInputChange} value={formData.first_name} required/>
          </div>

          <div>
            <label>Last Name</label>
            <input type="text" className='form-control' id='lName' name='last_name' onChange={handleInputChange} value={formData.last_name} required/>
          </div>
          
          <div>
            <label>Email</label>
            <input type="email" className='form-control' id='email' name='email' onChange={handleInputChange} value={formData.email} required/>
          </div>
          
          <div>
            <label>Password</label>
            <input type="password" className='form-control' id='pwd' name='password' minLength='4' onChange={handleInputChange} value={formData.password} required/>
          </div>

          <button type='submit' className='btn btn-primary mt-3 mb-3'>
            Submit
          </button>

          <div>
            <p><a href='LogIn' className='link-primary text-decoration-underline' >Have An Account?</a></p>
          </div>
          
        </form>
      </div>
    </>
  )
}

export default Register;