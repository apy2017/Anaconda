/**
 * Created by Greshilov on 16.05.2017.
 */
import React, { Component } from 'react'
import {ListGroupItem, Badge} from 'reactstrap'
import InlineEdit from 'react-edit-inline';
import queryString from 'query-string';
import DeleteImg from '../../assets/img/delete.png';
import getCookie from '../Service'

class Question extends Component {

    constructor(props) {
        super(props);
        this.dataChanged = this.dataChanged.bind(this);
        this.state = {
            pk: props.pk,
            caption: props.caption
        };
    }

    componentDidMount() {

    }

    componentWillReceiveProps(nextProps) {
        // You don't have to do this check first, but it can help prevent an unneeded render
        if (nextProps.caption !== this.state.caption) {
            this.setState({ pk: nextProps.pk, caption: nextProps.caption });
        }
    }

    dataChanged(data) {
        this.setState({
            caption: data.caption
        });
        this.updateOnServer(this.props.index, data.caption);

    }

    async updateOnServer(index, caption) {
        this.props.onChange(index, caption);
        var what = await fetch(`/api/v0/questions/${this.state.pk}/edit/`,
            {   method: 'POST',
                headers: {'Content-Type':'application/json',
                          'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({'action': 'edit', 'caption': caption})
            }

        ).then(response =>response.json());
        console.log(what);
    }

    async deleteOnServer(index) {
        this.props.onDelete(index);
        var what = await fetch(`/api/v0/questions/${this.state.pk}/edit/`,
            {   method: 'POST',
                headers: {'Content-Type':'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                credentials: 'include',
                body: JSON.stringify({'action': 'delete'})
            }

        ).then(response =>response.json());
    }
/*
    customValidateText(text) {
        return (text.length > 0 && text.length < 64);
    }
*/
    render () {
        return (
            <ListGroupItem className="justify-content-between">
                <InlineEdit
                    activeClassName="editing"
                    text={this.state.caption}
                    paramName="caption"
                    change={this.dataChanged}
                />
                <div className="justify-content-end">
                    <img className="icon" src={DeleteImg} onClick={() => {this.deleteOnServer(this.state.pk);}}/>
                </div>
            </ListGroupItem>
        );
    }
}

export default Question