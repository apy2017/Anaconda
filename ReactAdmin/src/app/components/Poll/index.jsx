import React, { Component } from 'react'
import InlineEdit from 'react-edit-inline';
import {ListGroupItem, Badge} from 'reactstrap'
import DeleteImg from '../../assets/img/delete.png';
import EditImg from '../../assets/img/edit.png';
import CodeImg from '../../assets/img/eye.png';
import {Link} from 'react-router-dom'

import getCookie from '../Service'

//import { Link } from 'react-router'
//import { format_date } from '../../utils'

class Poll extends Component {
    constructor(props) {
        super(props);
        this.dataChanged = this.dataChanged.bind(this);
        this.state = {
            pk: props.pk,
            name: props.name,
            code: props.code,
            owner: props.owner,
            passes: props.passes
        };
    }

    dataChanged(data) {
        this.setState({
            name: data.name
        });
        this.updateOnServer(this.props.index, data.name);

    }

    copyCodeToClipboard() {

    }

    async updateOnServer(index, name) {
        this.props.onChange(index, name);
        var what = await fetch(`/api/v0/polls/${this.state.pk}/edit/`,
            {   method: 'POST',
                headers: {'Content-Type':'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({'action': 'edit', 'name': name})
            }

        ).then(response =>response.json());
        console.log(what);
    }

    async deleteOnServer(index) {
        this.props.onDelete(index);
        var what = await fetch(`/api/v0/polls/${this.state.pk}/edit/`,
            {   method: 'POST',
                headers: {'Content-Type':'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({'action': 'delete'})
            }

        ).then(response =>response.json());
    }

    render () {
        return (
            <ListGroupItem className="justify-content-between">
                <InlineEdit
                    activeClassName="editing"
                    text={this.state.name}
                    paramName="name"
                    change={this.dataChanged}
                />
                <div className="justify-content-end">
                    <Badge>{this.state.code}</Badge>
                    <Badge pill>{this.state.passes}</Badge>
                    <img className="icon" src={CodeImg} onClick={() => {this.props.appendAnswers(this.state.name, this.state.code);}}/>
                    <img className="icon" src={EditImg} onClick={() => {this.props.appendQuestions(this.state.name, this.state.code);}}/>
                    <img className="icon" src={DeleteImg} onClick={() => {this.deleteOnServer(this.props.index);}}/>
                </div>
            </ListGroupItem>
        );
    }

}


export default Poll
