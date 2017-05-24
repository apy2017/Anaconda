/**
 * Created by Slava on 10.05.2017.
 */
import React, { Component } from 'react'
import { BrowserRouter, Route } from 'react-router-dom'
import { BaseLayout } from '../../layouts'
import User from '../User'


class App extends Component {
    render(){
        return(
            <BrowserRouter>
                <Route path="/" component={BaseLayout}/>
            </BrowserRouter>
    );
    }
}


export default App