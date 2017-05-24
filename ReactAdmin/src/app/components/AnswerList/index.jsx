/**
 * Created by Greshilov on 16.05.2017.
 */
import React, {Component} from 'react'
import Question from '../Question'
import {Button, Modal, ModalHeader, ModalBody, ModalFooter, Row, Col} from 'reactstrap';
import {Link} from 'react-router-dom'
import Answer from '../Answer'
import getCookie from '../Service'

class AnswerList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            answerList: [],
            modal: false,
            pk: this.props.pk,
            code: this.props.code,
            telegram_username: this.props.telegram_username
        };
        this.toggle = this.toggle.bind(this);
    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
        this.props.onClose;
    }

    async loadQuestions(pk) {
        this.setState({
            answerList: await fetch(`/api/v0/answerContainers/${pk}/`, {credentials: 'include'}).then(response =>response.json())
        })
    }

    componentDidMount() {
        this.loadQuestions(this.state.pk);
        this.toggle();
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            pk: nextProps.pk,
            telegram_user: nextProps.telegram_user
        });
        this.loadQuestions(nextProps.pk);
        this.toggle();
    }

    render() {
        const answerList = this.state.answerList.slice().sort((answerA, answerB) => {return answerA.pk > answerB.pk;});
        var listItems = answerList.map((answer, index) =>
            <Answer index={index}
                      key={answer.pk} pk={answer.pk}
                      caption={answer.caption}
                      on_question={answer.on_question.caption}
            />
        );
        if (!listItems.length) {
            listItems = <Row className="text-center"><h3>No answers on this poll yet.</h3></Row>;
        }
        return (
            <div className="questionList">
                <Modal isOpen={this.state.modal} toggle={this.toggle} className={this.props.className}>
                    <ModalHeader toggle={this.toggle}>{this.state.telegram_username} | Ответы</ModalHeader>
                    <ModalBody>
                        <Row className="full-width header-margin">
                            <Col sm="6" className="text-center right-border">
                                Ответ
                                </Col>
                            <Col sm="6" className="text-center">
                                Вопрос
                            </Col>
                        </Row>
                        {listItems}
                    </ModalBody>
                    <ModalFooter>
                        <Button color="secondary" onClick={this.toggle}>Закрыть</Button>
                    </ModalFooter>
                </Modal>
            </div>
        );
    }
}

export default AnswerList

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