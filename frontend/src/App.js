import React from 'react';
import { Switch, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// Importamos nuestros componentes previamente creados.
import AddTodo from './components/add-todo';
import TodosList from './components/todos-list';
import Login from './components/login';
import Signup from './components/signup'; 

// Importamos componentes de react-bootstrap
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar'; 
import Container from 'react-bootstrap/Navbar'; 

function App() {

  // Implementacion del login/signup con UseState 
  const [user, setUser] = React.useState(null);
  const [token, setToken] = React.useState(null);
  const [error, setError] = React.useState(''); 
  
  async function login(user = null){ //Default user = null 
    setUser(user); 
  }

  async function logout(){
    setUser(null); 
  }

  async function signup(user = null){
    setUser(user); 
  }
   
  return (
    <div className="App">
      <Navbar bg="primary" variant="dark">
        <div className="container-fluid">
          <Navbar.Brand href="#home">TodosApp</Navbar.Brand>
            <Nav className="me-auto">
              <Container>
                <Link class="nav-link" to={"/todos"}>Todos</Link>
                { user ? (
                  <Link class="nav-link"> Logout ({user})</Link>
                ) : (
                  <>
                    <Link class="nav-link" to={"/login"}>Login</Link>
                    <Link class="nav-link" to={"/signup"}>Sign Up</Link> 
                  </> 
                ) }
              </Container>
            </Nav> 
        </div>
      </Navbar> 
    </div>
  ); 
}

export default App; 
