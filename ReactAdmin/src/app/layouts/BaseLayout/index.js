import React from 'react';
import { Container, Row, Col } from 'reactstrap';
import SideBar from './SideBar'
import Navigation from './NavBar'

import styles from './layout.css';

export default class BaseLayout extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div>
                <Navigation/>
                <Container fluid>
                    <Row>
                        <Col sm="3" md="2" className="hidden-xs-down bg-faded sidebar"> <SideBar bg-inverse/> </Col>
                        <Col sm={{ size: 9, offset: 3}} md={{ size: 10, offset: 2}}>
                            <h1>Dashboard</h1>
                            <hr>
                        </Col>
                    </Row>
                </Container>
            </div>
        );
    }
}