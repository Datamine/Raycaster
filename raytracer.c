corner coordinates (x0, y0, z0); (x1, y1, z1) where _1 > _0

double ox = ray.o.x;
double oy = ray.o.y;
double oz = ray.o.z;

double dx = ray.d.x;
double dy = ray.d.y;
double dz = ray.d.z;

double tx_min;
double ty_min;
double tz_min;

double tx_max;
double ty_max;
double tz_max;

double a = 1.0 / dx
if (a >= 0){
    tx_min = (x0 - ox) * a;
    tx_max = (x1 - ox) * a;
}
else{
    tx_min = (x1 - ox) * a;
    tx_max = (x0 - ox) * a;
}

double b = 1.0/dy
if (b >= 0){
    ty_min = (y0 - oy) * a;
    ty_max = (y1 - oy) * a;
}
else{
    ty_min = (y1 - oy) * a;
    ty_max = (y0 - oy) * a;
}

double c = 1.0/dz
if (c >= 0){
    tz_min = (z0 - oz) * a;
    tz_max = (z1 - oz) * a;
}
else{
    tz_min = (z1 - oz) * a;
    tz_max = (z0 - oz) * a;
}

double t0, t1;

// find largest entering t value

if (tx_min > ty_min)
    t0 = tx_min;
else
    t0 = ty_min;
if t0 > tz_min
    t0 = tz_min;

if (tx_max > ty_max)
    t1 = tx_max;
else
    t1 = ty_min;
if tz_max > t1
    t1 = tz_max;

if (t0 < t1 && t1 > kEpsilon)
    return t0
else
    return null