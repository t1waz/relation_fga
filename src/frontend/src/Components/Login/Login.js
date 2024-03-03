import React, { useState} from 'react'
import "./Login.css"
import { MdEmail } from "react-icons/md";
import { TbPassword } from "react-icons/tb";
import logo_big from "../../Assets/RelFGA-logo.png";
import axios from 'axios';


export function Login() {
    const [values, setValues] = useState({
        email: "",
        password: "",
    });

    const handleInput = (event) => {
        const { name, value } = event.target;
        setValues(prev => ({ ...prev, [name]: value }));
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(values);
        axios.post('http://0.0.0.0/api/auth/obtain-token', JSON.stringify(values), {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(res => console.log(res))
            .catch(err => console.log(err));
    }

    return (
        <div className='login'>
            <div className='logo'>
                <img src={logo_big} alt=""/>
            </div>
            <div className='container'>

                <div className='header'>
                    <div className="text">RelFGA</div>
                    <div className="underline"></div>
                </div>
                <div className="inputs">
                    <div className="input">
                        <div className="image">
                            <MdEmail/>
                        </div>
                        <input name="email" type="email" placeholder="Email" onChange={handleInput}/>
                    </div>
                    <div className="input">
                        <div className="image">
                            <TbPassword/>
                        </div>
                        <input name="password" type="text" placeholder="Password" onChange={handleInput}/>
                    </div>
                </div>

                <button className="hover-button" onClick={handleSubmit}>Login</button>
                <button className="hover-button">Sign In</button>
            </div>
        </div>
    )
}
