import './App.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Landing from './pages/Landing';
import Register from './pages/Register';
import LogIn from './pages/LogIn';

const router = createBrowserRouter([
  { path: '/', element: <Register /> },
  { path: '/LogIn', element: <LogIn /> },
  { path: '/Landing', element: <Landing /> }
])

function App() {

  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App