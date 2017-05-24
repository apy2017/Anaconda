import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import { Nav, NavItem, NavLink } from 'reactstrap';

export default class SideBar extends React.Component {
    render() {
        return (
            <div>
                <p>Menu</p>
                <Nav vertical>
                    <NavItem>
                        <NavLink href="/main/">My polls</NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink href="#">Statistics</NavLink>
                    </NavItem>
                    <NavItem>
                        <NavLink disabled href="#">Disabled Link</NavLink>
                    </NavItem>
                </Nav>
                <hr />
                <p>About</p>
                <Nav vertical>
                    <NavLink href="#">Link</NavLink> <NavLink href="#">Link</NavLink> <NavLink href="#">Another Link</NavLink> <NavLink disabled href="#">Disabled Link</NavLink>
                </Nav>
            </div>
        );
    }
}