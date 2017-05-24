/**
 * Created by Greshilov on 17.05.2017.
 */
import React, {Component} from 'react'
import {ListGroupItem, ListGroup, Badge} from 'reactstrap'
import {Container, Row, Col, Button} from 'reactstrap';
import QuestionList from '../QuestionList'
import AnswerContainer from '../AnswerContainer'
import AnswerList from '../AnswerList'
import getCookie from '../Service'


class AnswerContainerList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            containerList: [],
            poll_code: this.props.poll_code,
            answerList: null
        };
    }

    onDelete(pk) {
        this.setState({
            containerList: this.state.containerList.filter((elem, index) => {
                return elem.pk != pk;
            })
        });
    }

    appendAnswers(pk, code, telegram_username) {
        this.setState({
            answerList: <AnswerList code={code} pk={pk} telegram_username={telegram_username}/>
        });
    }

    async loadContainers() {
        this.setState({
            containerList: await fetch(`/api/v0/answerContainers/`, {credentials: 'include'}).then(response =>response.json())
        });
    }


    componentDidMount() {
        this.loadContainers();
    }

    render() {
        const containerList = this.state.containerList.slice().sort((containerA, containerB) => {
            return containerA.pk > containerB.pk;
        });
        var listItems = containerList.map((container, index) =>
            <AnswerContainer index={index}
                             key={container.pk}
                             pk={container.pk}
                             on_poll={container.on_poll.name}
                             telegram_username={container.telegram_username}
                             
                             appendAnswers={(pk, code, telegram_username) => this.appendAnswers(pk, code, telegram_username)}
                             onDelete={pk => this.onDelete(container.pk)}/>
        );
        var answerList = this.state.answerList;
        if (!listItems.length) {
            listItems = <Row className="text-center"><h3>Нет пройденных опросов.</h3></Row>;
        }
        return (
            <div>
                <ListGroup>
                    {listItems}
                    <hr/>
                </ListGroup>
                {answerList}
            </div>
        );
    }
}

export default AnswerContainerList

/*
 <Link to={`${this.props.match.url}${poll.code}`}>
 <img className="icon" src={LogoImg}/>
 </Link>
 */