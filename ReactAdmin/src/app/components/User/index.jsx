import React, { Component } from 'react'
import Poll from '../Poll/index'

class User extends Component {
   constructor(props) {
                super(props);
                this.state = {polls: []};
    }

   async loadPolls() {
       this.setState({
           polls: await fetch("/api/v0/users/6674432/polls?format=json").then(response =>response.json())
       })
   }

   componentDidMount() {
       this.loadPolls();
   }

   render(){
       return(
           <ul className="content-list">
               {this.state.polls.map((poll, index) => (
                   <li className="content-list__item" key={index}>
                       <Poll poll={poll} />
                   </li>
               ))}
           </ul>
       );
   }
 }
 
 export default User
 
