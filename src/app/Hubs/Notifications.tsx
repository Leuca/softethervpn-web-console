import React from 'react';
import { Alert, AlertGroup, AlertActionCloseButton, AlertVariant } from '@patternfly/react-core';

class ToastAlertGroup extends React.Component { // pass a boolean 'add' to the class and remember to make it false to avoid continuing spawining alerts at every click
  constructor(props: Readonly<RouteComponentProps<{ tag: string }>>) {
    super(props);
    this.state = { alerts: [] };
    this.addAlert = (title, variant, child, key) => {
      this.setState({
        alerts: [ ...this.state.alerts, { title: title, variant: variant, child: child, key }]
      });
    };
    this.removeAlert = key => {
      this.setState({ alerts: [...this.state.alerts.filter(el => el.key !== key)] });
    };

  }

  UNSAFE_componentWillReceiveProps(nextProps: Readonly<RouteComponentProps<{ tag: string }>>): void {
      if(nextProps.add){
        this.addAlert(nextProps.title, nextProps.variant, nextProps.child, () => (new Date().getTime()));
      }
   }

  render(): React.Fragment {
    // const btnClasses = ['pf-c-button', 'pf-m-secondary'].join(' ');
    // const getUniqueId = () => (new Date().getTime());
    // const addSuccessAlert = () => { this.addAlert('Toast Success Alert', 'success', getUniqueId()) };
    // const addDangerAlert = () => { this.addAlert('Toast Danger Alert', 'danger', getUniqueId()) };
    // const addInfoAlert = () => { this.addAlert('Toast Info Alert', 'info', getUniqueId()) };


    return (
      <React.Fragment>
        <AlertGroup isToast>
          {this.state.alerts.map(({key, variant, child, title}) => (
            <Alert
              timeout={5000}
              isLiveRegion
              variant={AlertVariant[variant]}
              title={title}
              actionClose={
                <AlertActionCloseButton
                  title={title}
                  variantLabel={`${variant} alert`}
                  onClose={() => this.removeAlert(key)}
                />
              }
              key={key} >
              {child}
              </Alert>
          ))}
        </AlertGroup>
      </React.Fragment>
    );
  }
}

export { ToastAlertGroup };
