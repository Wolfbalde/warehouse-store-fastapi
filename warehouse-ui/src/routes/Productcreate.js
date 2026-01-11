import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Productcreate.css"

const BASE_URL='http://localhost:8000'

export const Productscreate = () => {
    const[name,setName] =useState('')
    const[price,setPrice] =useState('')
    const[quantity,setQuantity] =useState('')
    const navigate=useNavigate()

    const handlecreate = (event) =>{
        event?.preventDefault()

        const jsonstring=JSON.stringify({name,price,quantity})

        const requestOptions={
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: jsonstring
        }

        fetch(BASE_URL + '/product' ,requestOptions)
        .then(response =>{
            if(!response.ok){
                throw response
            }
        })
        .then(data =>{
            navigate('/')
        })
        .catch(error =>{
            console.log(error);            
        })
    }

    return (
        <div className="new_product_body">
            <div className="new_product_title">
                <div className="form-group">
                    <div>
                        <input className="input-1" placeholder="Name" onChange={(event) => setName(event.target.value)}/>
                    </div>
                </div>
                <div className="form-group">
                    <div>
                        <input className="input-1" placeholder="Price" onChange={(event) => setPrice(event.target.value)}/>
                    </div>
                </div>
                <div className="form-group">
                    <div>
                        <input className="input-1" placeholder="Quantity" onChange={(event) => setQuantity(event.target.value)}/>
                    </div>
                </div>
                <div>
                    <button className="button-4" onClick={handlecreate}>Create Product</button>
                </div>
            </div>
        </div>
    )
}