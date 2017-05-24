import React, {Component} from 'react'
import InlineEdit from 'react-edit-inline';
import {ListGroupItem, Badge} from 'reactstrap'
import DeleteImg from '../../assets/img/delete.png';
import EditImg from '../../assets/img/edit.png';
import CodeImg from '../../assets/img/eye.png';
import {Link} from 'react-router-dom'

import getCookie from '../Service'

class AnswerContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pk: props.pk,
            on_poll: props.on_poll,
            telegram_username: props.telegram_username
        };
    }

    async deleteOnServer(index) {
        this.props.onDelete(index);
        var what = await fetch(`/api/v0/answerContainers/${this.state.pk}/edit/`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({'action': 'delete'})
            }
        ).then(response =>response.json());
    }

    render() {
        var poll_caption = null;
        if (this.state.on_poll) {
            poll_caption = <b> - {this.state.on_poll}</b>;
        }
        return (
            <ListGroupItem className="justify-content-between">
                <div>Результат опроса пользователя <b>{this.state.telegram_username}</b> {poll_caption}</div>
                <div className="justify-content-end">
                    <img className="icon" src={CodeImg}
                         onClick={() => {this.props.appendAnswers(this.state.pk, this.state.on_poll, this.state.telegram_username);}}/>
                    <img className="icon" src={DeleteImg} onClick={() => {this.deleteOnServer(this.props.index);}}/>
                </div>
            </ListGroupItem>
        );
    }

}


export default AnswerContainer