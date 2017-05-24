/**
 * Created by Slava on 10.05.2017.
 */
import React, { Component } from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { BaseLayout } from '../../layouts'
import { Button, Col} from 'reactstrap';
import QuestionList from '../QuestionList'
import AnswerContainerList from '../AnswerContainerList'
import PollList from '../PollList'
import User from '../User'

class App extends Component {
    render(){
        return(
            <Router>
                <BaseLayout>
                     <Route exact path="/main/" component={PollList}/>
                     <Route exact path="/main/answers/" component={AnswerContainerList}/>
                </BaseLayout>
            </Router>
    );
    }
}


export default App
