/**
 * Created by Greshilov on 16.05.2017.
 */
import React, {Component} from 'react'
import {ListGroupItem, Badge, Row, Col} from 'reactstrap'

class Answer extends Component {

    constructor(props) {
        super(props);
        this.state = {
            pk: props.pk,
            caption: props.caption,
            on_question: props.on_question
        };
    }


    render() {
        return (
            <ListGroupItem>
                <Row className="full-width">
                    <Col sm="6" className="text-center">
                        {this.state.caption}
                    </Col>
                    <Col sm="6" className="text-center">
                        {this.state.on_question}
                    </Col>
                </Row>
            </ListGroupItem>
        );
    }
}

export default Answer