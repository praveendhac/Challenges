#!/usr/bin/env python

import os,sys
import argparse
import json
from geopy.distance import great_circle
from geopy.distance import geodesic 
from geopy.distance import vincenty 

def get_distance(office_location, customer_location):
  geodesic_dist = 0
  vincenty_dist = 0
  great_circle_dist = 0
  print "Calculate distance between office ", office_location, "and Customer location ", customer_location
  print "great circle: ", great_circle(tuple(office_location),tuple(customer_location)).kilometers
  geodesic_dist = geodesic(office_location,customer_location).kilometers
  vincenty_dist = vincenty(office_location,customer_location).kilometers
  great_circle_dist = great_circle(tuple(office_location),tuple(customer_location)).kilometers
  return geodesic_dist, vincenty_dist, great_circle_dist

def get_customer_data(cli_args):
  customer_file = cli_args.customer_file
  selected_customers = {}
  line_count = 0
  cust_count = 0
  with open(customer_file, 'r') as f:
    for line in f:
      customer = line
      try:
        customer = json.loads(line)
      except ValueError as verror:
        print "v continue:", verror, "for customer: ", customer
        continue

      try:
        customer_user_id = customer["user_id"]
        customer_location = [float(customer["latitude"]), float(customer["longitude"])]
      except (KeyError, ValueError) as kverror:
        print "%s from \"%s\"" % (kverror, str(customer).strip())
        continue

      is_valid_location = validate_coordinates(customer_location)
      if is_valid_location:
        dgeodesic, dvincenty, dgreat_circle = get_distance(cli_args.office_location, customer_location)
        if dgeodesic < 100:
          print "customer:", customer
          selected_customers[customer["user_id"]] = [customer["name"]]
          selected_customers[customer["user_id"]].append(dgeodesic)
          selected_customers[customer["user_id"]].append(dvincenty)
          selected_customers[customer["user_id"]].append(dgreat_circle)
          cust_count += 1
        line_count += 1
      else:
        print "Invalid location for customer ", customer["name"]
  print "total valid lines: ", line_count
  ordered_cust = sorted(selected_customers.keys())
  print "selected_customers:", selected_customers
  print "%4s\t\t%-16s\t\t%-8s" % ("User ID", "Customer Name", "Distance from Office(in kms)([geodesic, vincenty,great_circle])")
  print "%4s\t%-16s\t\t%-8s" % ("________", "____________", "__________________________")
  for uid in ordered_cust:
    print "%4s\t\t%-16s\t\t\t%-8s" % (uid, str(selected_customers[uid][0]), str(selected_customers[uid][1:]))
  print "Selected Customers count:", cust_count, "len(selected_customers):", len(selected_customers)

def main(location_args):
  print "Coordinates:",location_args.office_location
  print "Customer file:", location_args.customer_file
  get_customer_data(location_args)

def validate_coordinates(office_coordinates):
  if office_coordinates[0] < -90 or office_coordinates[0] > 90:
    print "Invalid Latitude: ", office_coordinates[0]
    return False

  if office_coordinates[1] < -180 or office_coordinates[1] > 180:
    print "Invalid Longitude: ", office_coordinates[1] 
    return False
    
  return True 

if __name__ == "__main__":
  cli_arg_parser = argparse.ArgumentParser(description="Calculate Great-circle distance between office and Customer")
  cli_arg_parser.add_argument("--office-location", nargs=2, type=float, default=[53.339428, -6.257664], help="Dublin office location lattitude, longitude")
  cli_arg_parser.add_argument("--customer-file", nargs="?", required=True, help="Customer record file")
  location_args = cli_arg_parser.parse_args()
  print "location_args:", location_args
 
  #print "Validating Coordinates:",location_args.office_location, "passed through CLI" 
  if not validate_coordinates(location_args.office_location):
    print "Entered invalid office coordinates!", location_args.office_location
    sys.exit() 

  if os.path.isfile(location_args.customer_file):
    main(location_args)
  else:
    print "file not present"
