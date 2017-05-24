/**
 * Created by Greshilov on 16.05.2017.
 */
import React, {Component} from 'react'
import Question from '../Question'
import {Button, Modal, ModalHeader, ModalBody, ModalFooter, Row} from 'reactstrap';
import {Link} from 'react-router-dom'
import getCookie from '../Service'

class QuestionList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            questionList: [],
            modal: false,
            code: this.props.code,
            name: this.props.name
        };
        this.toggle = this.toggle.bind(this);
        this.onClose = this.onClose.bind(this);
    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
    }

    onClose() {
        this.props.onClose();
        this.toggle();
    }

    onChange(index, caption) {
        var newQuestions = this.state.questionList.slice();
        newQuestions[index].caption = caption;
        this.setState({ questionList: newQuestions});
    }

    onDelete(pk) {
        this.setState({ questionList: this.state.questionList.filter((elem, index) => { return elem.pk != pk;} ) });
    }

    async addQuestion() {
        var question = await fetch(`/api/v0/polls/${this.state.code}/addQuestion/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({})
            }
        ).then(response =>response.json());
        var newQuestionList = this.state.questionList.slice();
        newQuestionList.push(question);
        this.setState({
            questionList: newQuestionList
        })
    }

    async loadQuestions(code) {
        this.setState({
            questionList: await fetch(`/api/v0/polls/${code}/`, {credentials: 'include'}).then(response =>response.json())
        })
    }

    componentDidMount() {
        this.loadQuestions(this.state.code);
        this.toggle();
    }

    componentWillReceiveProps(nextProps) {
        this.setState({
            code: nextProps.code,
            name: nextProps.name
        });
        this.loadQuestions(nextProps.code);
        this.toggle();
    }

    render() {
        const questionList = this.state.questionList.slice().sort((questionA, questionB) => {return questionA.pk > questionB.pk;});
        var listItems = questionList.map((question, index) =>
            <Question index={index}
                      key={question.pk} pk={question.pk}
                      caption={question.caption}
                      onChange={(index, caption) => this.onChange(index, caption)}
                      onDelete={pk => this.onDelete(question.pk)}/>
        );
        if (!listItems.length) {
            listItems = <Row className="text-center"><p>Нет вопросов в данном опросе.</p></Row>;
        }
        return (
            <div className="questionList">
                <Modal isOpen={this.state.modal} toggle={this.toggle} className={this.props.className}>
                    <ModalHeader toggle={this.onClose}>{this.state.name} | Редактирование</ModalHeader>
                    <ModalBody>
                        {listItems}
                    </ModalBody>
                    <ModalFooter>
                        <Button color="primary" onClick={() => {this.addQuestion()}}>Добавить вопрос</Button>
                        <Button color="secondary" onClick={this.onClose}>Закрыть</Button>
                    </ModalFooter>
                </Modal>
            </div>
        );
    }
}

export default QuestionList

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