import React from 'react';
import { Collapse, Navbar, NavbarToggler, NavbarBrand, Nav, NavItem, NavLink } from 'reactstrap';
import { Link } from 'react-router-dom';

export default class Navigation extends React.Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }
    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }
    render() {
        return (
            <div>
                <Navbar color="faded" light toggleable>
                    <NavbarToggler right onClick={this.toggle} />
                    <Link to="/main/"><NavbarBrand>TechBot | MailRu</NavbarBrand></Link>
                    <Collapse isOpen={this.state.isOpen} navbar>
                        <Nav className="ml-auto" navbar>
                            <NavItem>
                                <Link to="/main/"><NavLink>Опросы</NavLink></Link>
                            </NavItem>
                            <NavItem>
                                <Link to="/main/answers/"><NavLink>Результаты опросов</NavLink></Link>
                            </NavItem>
                            <NavItem>
                                <NavLink href="https://github.com/apy2017/Anaconda">Github</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink href="/logout/">Выход</NavLink>
                            </NavItem>
                        </Nav>
                    </Collapse>
                </Navbar>
            </div>
        );
    }
}