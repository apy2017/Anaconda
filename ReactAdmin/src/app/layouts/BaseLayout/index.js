import React from 'react';
import {Container, Row, Col, Button} from 'reactstrap';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import Navigation from './NavBar'
import PollList from '../../components/PollList'
import 'bootstrap/dist/css/bootstrap.css'

import styles from './layout.css';

export default class BaseLayout extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            child: []
        };
    }

    columnOpen(children) {
        this.setState({
                child: children
            }
        )
    }

    resize() {
        this.forceUpdate();
    }

    render() {
        var scope = this;
        return (
            <div>
                <Navigation/>
                <Container className="item-container rounded-bottom">
                    <Row>
                        <Col>
                            {this.props.children}

                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}