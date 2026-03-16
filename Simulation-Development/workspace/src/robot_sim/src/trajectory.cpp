#include "robot_sim/robot_drive.hpp"
#include <cmath>

// THIS FUNCTION RUNS EVERY 50ms AFTER THE SIMULATION IS STARTED
void RobotDrive::update_pose()
{
    t += 0.05;
    double dt=0.05;
    double yaw=0;
    double v_mag = sqrt(v_x*v_x +v_y*v_y);
    if(t<=f_time) {
        double N=mass*g;
        double F_fric_x=0.0;
        double F_fric_y=0.0;
        if(v_mag> 1e-6){
            F_fric_x= -mu*N*v_x/v_mag;
            F_fric_y= -mu* N*v_y/v_mag;
        }
        else {
            v_x=0;
            v_y=0;
        }
        double F_net_x=F_x+F_fric_x;
        double F_net_y=F_y+F_fric_y;
        double a_x=F_net_x/mass;
        double a_y=F_net_y/mass;
        x+=v_x*dt+ (a_x*dt*dt)/2;
        y+=v_y*dt+ (a_y*dt*dt)/2;
        v_x=v_x+a_x*dt;
        v_y=v_y+a_y*dt;
    }
    else {
        double N=mass*g;
        double F_net_x=0.0;
        double F_net_y=0.0;
        if(v_mag> 1e-6){
            F_net_x=- mu*N*v_x/v_mag;
            F_net_y= -mu* N*v_y/v_mag;
            double a_x=F_net_x/mass;
            double a_y=F_net_y/mass;
            x+=v_x*dt+ (a_x*dt*dt)/2;
            y+=v_y*dt+ (a_y*dt*dt)/2;
            v_x=v_x+a_x*dt;
            v_y=v_y+a_y*dt;
        }
        else{
            v_x=0;
            v_y=0;
        }
    }
    setPose(x, y, yaw); // USE THIS FUNCTION TO UPDATE THE POSE OF YOUR this.
}
