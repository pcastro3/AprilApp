import { useState } from 'react';
import Api from '../Api';

function LogIn() {

  const [formLoginData, setFormLoginData] = useState({
    email: '',
    password: ''
  })

  const handleInputChange = (event) => {
    setFormLoginData({
      ...formLoginData,
      [event.target.name]: event.target.value
    })
  }

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await Api.post('/users/login/', formLoginData);

    setFormLoginData({
      first_name: '',
      last_name: '',
      email: '',
      password: ''
    })
  }  

  return (
    <>
      <h1 className='mb-5'>Log In</h1>
      <div className="formContainer">
        <form onSubmit={handleFormSubmit}>
          
          <div>
            <label>Email</label>
            <input type="email" className='form-control' id='email' name='email' onChange={handleInputChange} value={formLoginData.email} required/>
          </div>
          
          <div>
            <label>Password</label>
            <input type="password" className='form-control' id='pwd' name='password' minLength='4' onChange={handleInputChange} value={formLoginData.password} required/>
          </div>

          <button type='submit' className='btn btn-primary mt-3 mb-3'>
            Submit
          </button>

          <div>
            <p><a href='/' className='link-primary text-decoration-underline' >Don&apos;t Have An Account?</a></p>
          </div>
          
        </form>
      </div>
    </>
  )
}

export default LogIn;