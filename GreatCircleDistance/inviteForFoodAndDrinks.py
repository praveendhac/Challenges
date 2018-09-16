#!/usr/bin/env python

import os,sys
import argparse
import logging as log
import json
import numpy

MEAN_EARTH_RADIUS = 6371

def get_distance(office_location, customer_location):
  log.info("Calculating distance between office %s and Customer location %s" % (office_location, customer_location))
  phi1 = numpy.radians(office_location[0])
  lambda1 = numpy.radians(office_location[1])
  phi2 = numpy.radians(customer_location[0])
  lambda2 = numpy.radians(customer_location[1])

  delta_lambda = lambda2-lambda1

  log.debug("Coordinates converted to radians phi1=%s phi2=%s lambda1=%s lambda2=%s" % (phi1, phi2, lambda1, lambda2))

  deltasigma = numpy.arccos(numpy.sin(phi1)*numpy.sin(phi2) + numpy.cos(phi1)*numpy.cos(phi2)*numpy.cos(delta_lambda))
  distance = MEAN_EARTH_RADIUS * numpy.degrees(deltasigma)/60
  log.info("Distance between Office and Customer is %f" % distance)
  return distance 

def validate_user_id(customer_user_id):
  return str(customer_user_id).isdigit()

def str2json(each_cust_line):
  cust_data_json = ""
  try:
    cust_data_json = json.loads(each_cust_line)
  except (KeyError, ValueError) as kverror:
    log.error("%s from \"%s\"" % (kverror, str(each_cust_line).strip()))
    return False 
  return cust_data_json

def process_customer_data(cli_args):
  customer_file = cli_args.customer_file
  selected_customers = {}
  cust_validLocationCount = 0
  lucky_cust_count = 0

  # open/process customer data file
  with open(customer_file, 'r') as f:
    for line in f:
      customer = str2json(line)
      if not customer:
        continue
 
      try:
        customer_user_id = customer["user_id"]
        customer_location = [float(customer["latitude"]), float(customer["longitude"])]
      except (KeyError, ValueError) as kverror:
        log.error("%s from \"%s\"" % (kverror, str(customer).strip()))
        continue

      is_valid_uid = validate_user_id(customer_user_id)
      if not is_valid_uid:
        log.error("Invalid user_id %s for customer \"%s\"" % (customer_user_id, customer["name"]))
        continue

      is_valid_location = validate_coordinates(customer_location)

      if is_valid_location:
        distance = get_distance(cli_args.office_location, customer_location)
        if distance < 100:
          selected_customers[customer["user_id"]] = [customer["name"]]
          selected_customers[customer["user_id"]].append(distance)
          lucky_cust_count += 1
        cust_validLocationCount += 1
      else:
        log.error("Invalid location %s for customer \"%s\"" % (customer_location, customer["name"]))
        continue

  log.info("Total Customers with valid locations: %d" % (cust_validLocationCount))
  ordered_cust = sorted(selected_customers.keys())
  log.info("Number of Customers selected for Food & Drinks: %s" % (selected_customers))
  print "%4s\t\t%-16s\t\t%-8s" % ("\nUser ID", "Customer Name", "Distance from Office(in kms)")
  print "%4s\t%-16s\t\t%-8s" % ("________", "____________", "__________________________")
  for uid in ordered_cust:
    print "%4s\t\t%-16s\t\t\t%-8s" % (uid, str(selected_customers[uid][0]), str(selected_customers[uid][1]))
  print "Total Customers Selected for Food & Drinks:", lucky_cust_count

def main(cli_args):
  log.info("Office Coordinates %s, customer data file is %s" % (cli_args.office_location, cli_args.customer_file))
  process_customer_data(cli_args)

def validate_coordinates(office_coordinates):
  if office_coordinates[0] < -90 or office_coordinates[0] > 90:
    log.error("Invalid Latitude, %f" % (office_coordinates[0]))
    return False

  if office_coordinates[1] < -180 or office_coordinates[1] > 180:
    log.error("Invalid Longitude, %f" % (office_coordinates[1]))
    return False
    
  return True 

if __name__ == "__main__":
  cli_arg_parser = argparse.ArgumentParser(description="Calculate Great-circle distance between Office and Customer location")
  cli_arg_parser.add_argument("--office-location", nargs=2, type=float, default=[53.339428, -6.257664], help="Dublin office location lattitude, longitude")
  cli_arg_parser.add_argument("--customer-file", nargs="?", required=True, help="Customer record file")
  cli_arg_parser.add_argument("-v","--verbose", help="enable verbose logging", action="store_true")
  cli_args = cli_arg_parser.parse_args()
  if cli_args.verbose:
    log.basicConfig(format="%(asctime)s %(levelname)s %(message)s", datefmt="%d-%m-%Y-%H:%M:%S %Z", level=log.DEBUG)
  else:
    log.basicConfig(format="%(asctime)s %(levelname)s %(message)s", datefmt="%d-%m-%Y-%H:%M:%S %Z")

  print "All CLI arguments passed:", cli_args
 
  log.info("Validating Coordinates: %s passed through CLI" % (cli_args.office_location)) 
  if not validate_coordinates(cli_args.office_location):
    log.error("Entered invalid office coordinates %s!" % (cli_args.office_location))
    sys.exit() 

  if os.path.isfile(cli_args.customer_file):
    main(cli_args)
  else:
    log.error("File not present. Check if file is present on disk.")
