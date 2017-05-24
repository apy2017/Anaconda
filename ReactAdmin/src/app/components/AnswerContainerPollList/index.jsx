/**
 * Created by Greshilov on 16.05.2017.
 */
import React, {Component} from 'react'
import Question from '../Question'
import {Button, Modal, ModalHeader, ModalBody, ModalFooter, Row} from 'reactstrap';
import {Link} from 'react-router-dom'
import AnswerContainer from '../AnswerContainer'
import AnswerList from '../AnswerList'
import getCookie from '../Service'

class AnswerContainerPollList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            answerList: [],
            answers: null,
            modal: false,
            poll_code: this.props.poll_code,
            name: this.props.name
        };
        this.toggle = this.toggle.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
        this.props.onClose;
    }


    onDelete(pk) {
        this.setState({ answerList: this.state.answerList.filter((elem, index) => { return elem.pk != pk;} ) });
    }

    onClose() {
        this.props.onClose();
        this.setState({
            answers: null
        });
        this.toggle();
    }

    appendAnswers(pk, code, telegram_username) {
        this.setState({
            answers: <AnswerList code={code} pk={pk} telegram_username={telegram_username}/>
        });
    }

    async loadAnswers(poll_code) {
        this.setState({
            answerList: await fetch(`/api/v0/polls/${poll_code}/answerContainers/`, {credentials: 'include'}).then(response =>response.json())
        })
    }

    componentDidMount() {
        this.loadAnswers(this.state.poll_code);
        this.toggle();
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            poll_code: nextProps.poll_code,
            name: nextProps.name
        });
        this.loadAnswers(nextProps.poll_code);
        this.toggle();
    }

    render() {
        const answerList = this.state.answerList.slice().sort((questionA, questionB) => {return questionA.pk > questionB.pk;});
        var listItems = answerList.map((answer, index) =>
            <AnswerContainer index={index}
                      key={answer.pk} pk={answer.pk}
                      telegram_username={answer.telegram_username}
                      appendAnswers={(pk, code, telegram_username) => this.appendAnswers(pk, code, telegram_username)}
                      onDelete={pk => this.onDelete(answer.pk)}/>
        );
        if (!listItems.length) {
            listItems = <Row className="text-center"><p>Нет результатов для данного опроса</p></Row>;
        }
        return (
            <div className="questionList">
                <Modal isOpen={this.state.modal} toggle={this.onClose} className={this.props.className}>
                    <ModalHeader>{this.state.name} | Ответы </ModalHeader>
                    <ModalBody>
                        {listItems}
                    </ModalBody>
                    <ModalFooter>
                        <a href={`/api/v0/polls/${this.state.poll_code}/answerContainers/xml`} target="_blank"><Button color="primary">Скачать XML</Button></a>
                        <Link to="/main/"><Button color="secondary" onClick={this.onClose}>Закрыть</Button></Link>
                    </ModalFooter>
                </Modal>
                {this.state.answers}
            </div>
        );
    }
}

export default AnswerContainerPollList

/*

 class QuestionList extends Component {

 constructor(props) {
 super(props);
 this.state = {
 questionList: []
 };
 }

 async loadQuestions(poll_id) {
 this.setState({
 questionList: await fetch(`/api/v0/polls/${poll_id}/`,{credentials: 'include'}).then(response =>response.json())
 })
 }

 componentDidMount() {
 console.log(this.props.match.params.poll_id);
 this.loadQuestions(this.props.match.params.poll_id);
 }

 render () {
 const listItems = this.state.questionList.map((question) =>
 <Question pk={question.pk} caption={question.caption}/>
 );
 return (
 <div className="questionList">
 {listItems}
 </div>
 );
 }
 }

 export default QuestionList
 */