/**
 * Created by Greshilov on 17.05.2017.
 */
import React, {Component} from 'react'
import {ListGroupItem, ListGroup, Badge} from 'reactstrap'
import {Container, Row, Col, Button} from 'reactstrap';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group'
import Poll from '../Poll'
import QuestionList from '../QuestionList'
import AnswerContainerPollList from '../AnswerContainerPollList'
import getCookie from '../Service'


class PollList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            pollList: [],
            questionList: null
        };
        this.closeQuestions = this.closeQuestions.bind(this);
    }

    onChange(index, caption) {
        var newPolls = this.state.pollList.slice();
        newPolls[index].name = caption;
        this.setState({pollList: newPolls});
    }

    onDelete(pk) {
        this.setState({
            pollList: this.state.pollList.filter((elem, index) => {
                return elem.pk != pk;
            })
        });
    }

    appendAnswers(name, poll_code) {
        this.setState({
            questionList: <AnswerContainerPollList poll_code={poll_code} name={name} onClose={() => this.closeQuestions()}/>
        });
    }

    appendQuestions(name, code) {
        this.setState({
            questionList: <QuestionList code={code} name={name} onClose={() => this.closeQuestions()}/>
        });
    }

    closeQuestions() {
        this.setState({
            questionList: null
        });
    }
    async loadPolls() {
        this.setState({
            pollList: await fetch(`/api/v0/polls/`, {credentials: 'include'}).then(response =>response.json())
        })
    }

    async addPoll() {
        var poll = await fetch(`/api/v0/polls/add/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({'name': 'Новый опрос (кликните, чтобы изменить текст)'})
            }
        ).then(response =>response.json());
        var newPollList = this.state.pollList.slice();
        newPollList.push(poll);
        this.setState({
                pollList: newPollList
            }
        )
    }

    componentDidMount() {
        this.loadPolls();
    }

    render() {

        const pollList = this.state.pollList.slice().sort((pollA, pollB) => {
            return pollA.pk > pollB.pk;
        });
        var listItems = pollList.map((poll, index) =>
            <Poll index={index}
                  key={poll.pk} pk={poll.pk}
                  name={poll.name}
                  code={poll.code}
                  passes={poll.passes}
                  appendAnswers={(name, poll_code) => this.appendAnswers(name, poll_code)}
                  appendQuestions={(name, code) => this.appendQuestions(name, code)}
                  onClose={() => this.closeQuestions()}
                  onChange={(index, caption) => this.onChange(index, caption)}
                  onDelete={pk => this.onDelete(poll.pk)}/>
        );
        if (!listItems.length) {
            listItems = <Row className="text-center"><h2>У вас нет ни одного опроса.</h2></Row>;
        }
        var questionList = this.state.questionList;
        return (
            <div>
            <ListGroup>
                {listItems}
                <hr/>
                <Button color="primary" onClick={() => {this.addPoll()}}>Добавить новый опрос</Button>
            </ListGroup>
                {questionList}
            </div>
        );
    }
}

export default PollList

/*
 <Link to={`${this.props.match.url}${poll.code}`}>
 <img className="icon" src={LogoImg}/>
 </Link>
 */